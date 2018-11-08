========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
    * - package
      - | |version| |supported-versions| |supported-implementations|
    * - license
      - | |license|

.. |travis| image:: https://travis-ci.org/0LL13/pdf2textbox.svg?branch=master
    :target: https://travis-ci.org/0LL13/pdf2textbox
    :alt: Travis-CI Build Status

.. |license| image:: https://img.shields.io/cocoapods/l/AFNetworking.svg
    :alt: CocoaPods

.. |docs| image:: https://readthedocs.org/projects/pytest-cov/badge/?style=flat
    :target: https://readthedocs.org/projects/pdf2textbox
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/pdf2textbox.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pdf2textbox

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pdf2textbox.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pdf2textbox

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pdf2textbox.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pdf2textbox

.. end-badges



pdf2textbox
============

A PDF-to-text converter based on pdfminer2 (which is based on
pdfminer.six which is based on pdfminer).
Converts PDF files with up to 3 columns and a header (optional)
to text and avoids most caveats that multi-columned PDF files have
in store for PDF conversion.


Features
--------

Convert PDF to text in the original order. This works well for PDF-files
without tables, graphs, and other stuff.

Allows command line parameter -s (--slice) to indicate that only part of
the PDF document is of interest. Start and end page will then be either
retreived from the document's name using '_' or '|' as delimiters or -
if start and end page cannot be found - user input is requested.


Installation
------------

    pip install pdf2textbox


Contribute
----------

- Issue Tracker: https://github.com/0LL13/pdf2textbox/issues
- Source: https://github.com/0LL13/pdf2textbox

Support
-------

Feel free to fork and improve.

Warranty
--------

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY
DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

License
-------

MIT License

Copyright (c) 2018 Oliver Stapel
