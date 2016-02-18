#!/usr/bin/env pthon
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 William Ewing.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""Formatter for GYP project files."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import ast
import contextlib
import json
import os
import sys


def load_gyp(infile):
    """Load a GYP project information to a file."""
    gyp_root = ast.literal_eval(infile.read())
    if not isinstance(gyp_root, dict):
        raise TypeError('Root object is not a dictionary.')
    return gyp_root


def dump_gyp(outfile, gyp_root):
    """Write an object to a file as formatted JSON."""
    json.dump(gyp_root, outfile,
              indent=4, separators=(',', ': '), sort_keys=True)


@contextlib.contextmanager
def replacefile(path, text=True):
    """Context manager for best-effort atomic file replacement."""
    tmp_path = '%s~' % path
    with open(tmp_path, 'w' if text else 'wb') as tmp_file:
        yield tmp_file
    os.remove(path)
    os.rename(tmp_path, path)


def main(argv=None):
    """Format some GYP project files."""

    # Parse arguments
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description='Format GYP project files.')
    parser.add_argument('-i', '--in-place', action='store_true',
                        help='Format files in-place.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='GYP project files to format.')
    args = parser.parse_args(argv)

    # Process files
    retv = 0
    for path in args.files:

        try:
            with open(path, 'rb') as infile:
                gyp_root = load_gyp(infile)

        except (IOError, ValueError, TypeError) as exc:
            retv = -1
            print('Error loading %r: %s' % (path, exc))
            continue

        try:
            if args.in_place:
                try:
                    with replacefile(path) as swp_file:
                        dump_gyp(swp_file, gyp_root)

                except IOError as exc:
                    print('Error updating %r: %s' % (path, exc))
                    retv = -1
                    continue

            else:
                dump_gyp(sys.stdout, gyp_root)

        except TypeError as exc:
            print('Error formatting %r: %s' % (path, exc))
            retv = -1
            continue

    # Return
    return retv

if __name__ == '__main__':
    exit(main())
