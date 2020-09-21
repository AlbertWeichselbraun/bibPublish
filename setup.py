#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
sys.path.insert(0, path.join(here, 'src'))

from bibPublish import (__version__, __author__, __author_email__, __license__)

# Get the long description from the README.md file
with open(path.join(here, 'README.rst')) as f:  # , encoding='utf-8'
    long_description = f.read()

setup(
    # Metadata
    name="bibPublish",
    version=__version__,
    description='bibPublish - publishes bibTex bibliographies.',
    long_description=long_description,
    author=__author__,
    author_email=__author_email__,
    python_requires='>=3.5',
    classifiers=[
           'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
           'Programming Language :: Python :: 3.5',
           'Programming Language :: Python :: 3.6',
           'Programming Language :: Python :: 3.7',
           'Programming Language :: Python :: 3.8',
    ],
    url='http://github.com/AlbertWeichselbraun/bibPublish',
    license=__license__,
    package_dir={'': 'src'},

    # Package List
    packages=find_packages('src'),

    # Scripts
    scripts=[
        'scripts/bibPublish.py'
    ],

    # Requirements
    install_requires=[
        'bibtexparser',
    ]
)
