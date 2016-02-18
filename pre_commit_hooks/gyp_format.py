#!/usr/bin/env python
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
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='GYP project files to format.')
    args = parser.parse_args(argv)

    # Process files
    retv = 0
    for path in args.files:
        # Read input
        try:
            gyp_text = open(path, 'rb').read()
            gyp_data = ast.literal_eval(gyp_text)
            if not isinstance(gyp_data, dict):
                raise TypeError('Root element is not a dictionary.')
        except (IOError, ValueError, TypeError) as exc:
            retv = 1
            print('Error loading %r: %s' % (path, exc))
            continue

        # Format output
        try:
            out_text = json.dumps(gyp_data, indent=4, separators=(',', ': '),
                                  sort_keys=True)
        except TypeError as exc:
            retv = 1
            print('Error formatting %r: %s' % (path, exc))
            continue

        # Check if they match
        if gyp_text == out_text:
            continue

        # Update output
        try:
            retv = 1
            with replacefile(path, text=False) as outfile:
                outfile.write(out_text)
        except (IOError, OSError) as exc:
            print('Error updating %r: %s' % (path, exc))

    # Return
    return retv

if __name__ == '__main__':
    exit(main())
