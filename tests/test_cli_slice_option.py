import io
import os
import pytest

from pdf2textbox.pdf2textbox import _get_pages
from pdf2textbox.pdf2textbox import _get_pdf_file
from pdf2textbox.pdf2textbox import _pdf_to_text_slice


@pytest.fixture()
def cmd_option_slice():
    '''will provide command line option -s (i.e. --slice)'''

    return '-s'


def test_cmd_option_slice(cmd_option_slice):
    '''test command line options'''

    assert cmd_option_slice == '-s'


def test_get_pages(cmd_option_slice):
    '''test command line options'''

    file_name = 'Id=MMP16%2F139_14622_14624.pdf'

    page_from, page_to = _get_pages(file_name, verbose=False)

    assert int(page_from) == 14622
    assert int(page_to) == 14624


def test_pdf_to_text_slice(cmd_option_slice):
    '''assert that sliced PDF file will be returned in a dictionary'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/Id=MMP16%2F139_14622_14624.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)

    page_from, page_to = _get_pages(pdf_loc, verbose=False)
    boxes = _pdf_to_text_slice(pdf, page_from, page_to, verbose=False)

    assert isinstance(boxes, dict)
