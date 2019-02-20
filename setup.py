#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import io
import pathlib
import re

from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from io import open

from setuptools import find_packages
from setuptools import setup


script_dir = pathlib.Path(__file__).parent.resolve()

with open(str(script_dir)+'/README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pdf2textbox',
    packages=['pdf2textbox/'],
    version = '0.4.1',
    description = 'A PDF-to-text converter based on pdfminer2',
    long_description = long_description,
    author = 'Oliver Stapel',
    author_email = 'hardy.ecc95@gmail.com',
    url='https://github.com/0LL13/pdf2textbox',
    license='MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX :: Linux',
        'Topic :: Text Processing :: General',
        ],
    keywords = 'PDF pdfminer2 PDFconversion text-processing',
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pdfminer2', 'requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'pdf2textbox = pdf2textbox:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/0LL13/pdf2textbox/issues',
        'Source': 'https://github.com/0LL13/pdf2textbox',
    },
)
