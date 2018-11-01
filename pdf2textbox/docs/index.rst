.. pdf2textbox documentation master file, created by
   sphinx-quickstart on Wed Apr 11 10:31:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


pdf2textbox's doc
=================

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

A PDF-to-text converter based on pdfminer2 (which is based on pdfminer.six which is based on pdfminer). Converts PDF files with up to 3 columns and a header (optional) to text and avoids many caveats that multi-columned PDF files have in store for PDF conversion.

Allows command line parameter -s (–slice) to indicate that only part of the PDF document is of interest. Start and end page will then be either retreived from the document’s name using ‘_’ or ‘|’ as delimiters or - if start and end page cannot be found - user input is requested.

.. seealso::
    
    Extract PDF-files with `pdfminer2 <https://pypi.python.org/pypi/pdfminer2>`_

What's the difference?
----------------------

While pdfminer2 works well for plain text there will be issues when that
text comes in two or more columns, when there are indented quotes, headers, 
and other options to edit text that are not uncommon. The solutions that 
can be found as yet (i.e. pyPDF, pdfminer2, pdfx, ...)

* ... will include headers into the text flow
* ... will return small or very small (DetailledAggregator) text units
* ... will return text from left to right without acknowledging the columns
* ... will mix text from different columns into one text flow

.. seealso::

    Stackoverflow hottest answer tagged `pdfminer <https://stackoverflow.com/a/44476759/6597765>`_

    Using `PDFx <https://www.metachris.com/pdfx/>`_

    Using `PyPDF2 <https://medium.com/@rqaiserr/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f>`_

    pdfminer using a `DetailedAggregator <https://stackoverflow.com/a/19179114/6597765>`_


pdf2textbox returns the extracted text in two meta structures: a dict that 
differentiates between 'header' and 'columns' and boxes similar to the paragraphs
of the original text  which makes the final conversion into a coherent and 
meaningful text document easier:

* Split text into coherent sentences
* Differentiate dots at the end of a sentence from dots behind dates, titles, etc.
* Allows simple regex routines to combine words seperated by hyphens (at linebreaks)
* Allign information from header to parts of text (i.e. page number, date, ...)

Graphs, tables, and other visual or graphic 2D blocks, and tocs will cause havock.

Features
--------

Convert PDF to text in the original order. This works well for PDF-files 
without tables, graphs, and other stuff.

After extracting the text in boxes, there still has to be run another
function to strip the text of special signs, zeroes and the like.

Note
----

Often the textboxes will NOT be identical with paragraphs of the PDF-file.
There might be cases when a textbox ends mid-sentence just to be
continued with the next box. This is due to the PDF file's graphic-oriented organization of content. However, the order of text will be correct.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
