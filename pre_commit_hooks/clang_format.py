#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 William Ewing.
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
"""Thin wrapper around clang-format."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import subprocess
import sys


def main(argv=None):
    """Format source files with clang-format."""

    # Parse arguments
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser('Format files with clang-format.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='Source files to format.')
    args = parser.parse_args(argv)

    # Run clang-format on the specified files.
    for path in args.files:
        subprocess.call(['clang-format', '-i', path])


if __name__ == '__main__':
    exit(main())
