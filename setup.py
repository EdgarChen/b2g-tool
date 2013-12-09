#!/usr/bin/env python
# vim:fileencoding=utf-8:noet

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
        README = open(os.path.join(here, 'README.md')).read()
except IOError:
        README = ''

# dependencies
deps = ['mozdevice >= 0.22']

setup(
        name='b2g-tool',
        version='beta',
        description='b2g debug tools',
        long_description=README,
        author='Edgar Chen',
        author_email='top12345tw@gmail.com',
        url='https://github.com/EdgarChen/b2g-tool',
        scripts=[
                'scripts/b2g-tool'
        ],
  packages=find_packages(),
  install_requires=deps,
)
