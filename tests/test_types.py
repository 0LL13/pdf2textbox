import io
import os
import requests

from pdf2textbox.pdf2textbox import _get_pdf_file
from pdf2textbox.pdf2textbox import _pdf_to_text_slice
from pdf2textbox.pdf2textbox import _pdf_to_text_all
from pdf2textbox.pdf2textbox import _get_page_layout

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines


def test_pdf_to_text_all():
    '''test type textbox is dict'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    file_loc = '{}/Id=MMP15%2F57_5694_5696.pdf'.format(loc)
    with open(file_loc, 'br') as pdf:
        textbox = _pdf_to_text_all(pdf, verbose=False)

    assert isinstance(textbox, dict)


def test_textbox_structure():
    '''test if textbox contains pages, header, left and right column'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    file_loc = '{}/Id=MMP15%2F57_5694_5696.pdf'.format(loc)
    with open(file_loc, 'br') as pdf:
        textbox = _pdf_to_text_all(pdf, verbose=False)

    for key, val in textbox.items():
        assert isinstance(key, int)
        assert isinstance(val, dict)
        for subkey, subval in val.items():
            assert subkey in ['header', 'left_column', 'right_column']
            assert isinstance(subval, list)
