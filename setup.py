#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='pre_commit_hooks',
    description='Some additional hooks for pre-commit.',
    url='https://github.com/TheEndarkenedOne/pre-commit-hooks',

    author='William Ewing',
    author_email='will.ewing.iv@gmail.com',

    entry_points={
        'console_scripts': [
            'gyp-format = pre_commit_hooks.gyp_format:main'
        ]
    }
)
