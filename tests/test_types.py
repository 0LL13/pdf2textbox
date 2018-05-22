import io
import os

from src.pdf2textbox.pdf2textbox import _get_pdf_file
from src.pdf2textbox.pdf2textbox import _get_textbox
from src.pdf2textbox.pdf2textbox import _extract_textboxes


def test_get_pdf_file():
    '''test type pdf is io.BytesIO stream'''

    url = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokumenent?Id=MMP16%2F8|368|369'
    pdf = _get_pdf_file(url)

    assert isinstance(pdf, io.BytesIO)


def test_get_textbox():
    '''test type textbox is dict'''

    #file_loc = './src/pdf2textbox/data/Id=MMP15%2F57|5694|5696.pdf'
    file_loc = './src/pdf2textbox/data/Id=MMP16%2F139|14622|14624.pdf'
    pdf = open(file_loc, 'br')
    textbox = _get_textbox(pdf)

    assert isinstance(textbox, dict)


def test_textbox_structure():
    '''test if textbox contains pages, header, left and right column'''

    file_loc = './src/pdf2textbox/data/Id=MMP15%2F57|5694|5696.pdf'
    pdf = open(file_loc, 'br')
    textbox = _get_textbox(pdf)

    for key, val in textbox.items():
        assert isinstance(key, int)
        assert isinstance(val, dict)
        for subkey, subval in val.items():
            assert subkey in ['header', 'left_column', 'right_column']
            assert isinstance(subval, list)
