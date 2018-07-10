#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from os import path
from io import open

from setuptools import find_packages
from setuptools import setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pdf2textbox',
    version = '0.2.4',
    description = 'A PDF-to-text converter based on pdfminer2',
    long_description = long_description,
    long_description_content_type='text/x-rst',
    author = 'Oliver Stapel',
    author_email = 'hardy.ecc95@gmail.com',
    url='https://github.com/0LL13/pdf2textbox',
    license='MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX :: Linux',
        'Topic :: Text Processing :: General',
        ],
    keywords = 'PDF pdfminer2 PDFconversion text-processing',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pdfminer2', 'requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'pdf2textbox = pdf2textbox:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/0LL13/pdf2textbox/issues',
        'Say Thanks!': 'https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg',
        'Source': 'https://github.com/0LL13/pdf2textbox',
    },
)
