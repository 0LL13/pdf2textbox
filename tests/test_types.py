import io
import os

from src.pdf2textbox.pdf2textbox import _get_pdf_file
from src.pdf2textbox.pdf2textbox import _pdf_to_text_slice
from src.pdf2textbox.pdf2textbox import _pdf_to_text_all
from src.pdf2textbox.pdf2textbox import _get_page_layout

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines


def test_pdf_to_text_all():
    '''test type textbox is dict'''

    file_loc = '../pdf2textbox/src/pdf2textbox/data/Id=MMP15%2F57_5694_5696.pdf'
    with open(file_loc, 'br') as pdf:
        textbox = _pdf_to_text_all(pdf, verbose=False)

    assert isinstance(textbox, dict)


def test_textbox_structure():
    '''test if textbox contains pages, header, left and right column'''

    file_loc = '../pdf2textbox/src/pdf2textbox/data/Id=MMP15%2F57_5694_5696.pdf'
    with open(file_loc, 'br') as pdf:
        textbox = _pdf_to_text_all(pdf, verbose=False)

    for key, val in textbox.items():
        assert isinstance(key, int)
        assert isinstance(val, dict)
        for subkey, subval in val.items():
            assert subkey in ['header', 'left_column', 'right_column']
            assert isinstance(subval, list)


def test_get_page_layout():
    '''assert that parameters VERTICAL and HORIZONTAL are boolean'''

    file_loc = '../pdf2textbox/src/pdf2textbox/data/Id=MMP15%2F57_5694_5696.pdf'
    with open(file_loc, 'br') as pdf:
        parser = PDFParser(pdf)
        document = PDFDocument(parser, password=None)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        VERTICAL = HORIZONTAL = False

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            LTPage = device.get_result()
            VERTICAL, HORIZONTAL = _get_page_layout(LTPage, VERTICAL, HORIZONTAL)
            assert isinstance(VERTICAL, bool)
            assert isinstance(HORIZONTAL, bool)
