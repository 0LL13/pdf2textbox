import io
import os
import re

from pdf2textbox.pdf2textbox import _get_pdf_file
from pdf2textbox.pdf2textbox import _pdf_to_text_all


def test_convert_text_only():
    '''assert that this file has one column and no header'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/01a_only_text.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    boxes = _pdf_to_text_all(pdf, verbose=False)

    assert boxes[1]['column']
    assert boxes[2]['column']


def test_convert_two_cols():
    '''assert that this file has two columns'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/02a_two_cols.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    boxes = _pdf_to_text_all(pdf, verbose=False)

    assert boxes[1]['left_column']
    assert boxes[1]['right_column']
    assert boxes[2]['column']


def test_convert_three_cols():
    '''assert that this file has three columns'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/03a_three_cols.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    boxes = _pdf_to_text_all(pdf, verbose=False)

    assert boxes[1]['left_column']
    assert boxes[1]['center_column']
    assert boxes[1]['right_column']
    assert boxes[2]['left_column']
    assert boxes[2]['right_column']


def test_convert_one_col_and_header():
    '''assert that this file has one column and a header'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/04a_text_and_header.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    boxes = _pdf_to_text_all(pdf, verbose=False)

    assert boxes[1]['header']
    assert boxes[1]['column']
    assert boxes[2]['header']
    assert boxes[2]['column']


def test_convert_two_cols_and_header():
    '''assert that this file has two columns and a header'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/05a_two_cols_and_header.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    boxes = _pdf_to_text_all(pdf, verbose=False)

    assert boxes[1]['header']
    assert boxes[1]['left_column']
    assert boxes[1]['right_column']
    assert boxes[2]['header']
    assert boxes[2]['column']


def test_convert_three_cols_and_header():
    '''assert that this file has three columns and a header'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/06a_three_cols_and_header.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    boxes = _pdf_to_text_all(pdf, verbose=False)

    assert boxes[1]['header']
    assert boxes[1]['left_column']
    assert boxes[1]['center_column']
    assert boxes[1]['right_column']
    assert boxes[2]['header']
    assert boxes[2]['left_column']
    assert boxes[2]['right_column']

