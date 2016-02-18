#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pre_commit_hooks',
    description='Some additional hooks for pre-commit.',
    url='https://github.com/TheEndarkenedOne/pre-commit-hooks',

    author='William Ewing',
    author_email='will.ewing.iv@gmail.com',

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gyp-format = pre_commit_hooks.gyp_format:main'
        ]
    }
)
