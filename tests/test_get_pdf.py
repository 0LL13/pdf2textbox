import io
import os
import re

from src.pdf2textbox.pdf2textbox import _get_pdf_file


def test_get_url():
    '''urls that can be chosen in _get_url should be valid url addresses'''

    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'

    urls = ['{}Id=MMP14%2F138|16018|16019'.format(base),
            '{}Id=MMP16%2F139|14617|14630'.format(base),
            '{}Id=MMP16%2F140|14760|14768'.format(base),
            '{}Id=MMP15%2F57|5694|5696'.format(base),
            '{}Id=MMP16%2F8|368|369'.format(base)]

    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    for url in urls:
        assert re.match(regex, url)


def test_get_local_file():
    '''local PDF files should exist'''

    pdf_locs = ['../pdf2textbox/src/pdf2textbox/data/three_col_horizontal.pdf',
                '../pdf2textbox/src/pdf2textbox/data/three_col_vertical.pdf',
                '../pdf2textbox/src/pdf2textbox/data/Id=MMP16%2F139_14622_14624.pdf',
                '../pdf2textbox/src/pdf2textbox/data/Id=MMP15%2F57_5694_5696.pdf']

    for loc in pdf_locs:
        assert os.path.isfile(loc)


def test_get_pdf_file_url():
    '''using requests test if type pdf is io.BytesIO stream'''

    url = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokumenent?Id=MMP16%2F8|368|369'
    pdf = _get_pdf_file(url, verbose=False)

    assert isinstance(pdf, io.BytesIO)


def test_get_pdf_file_local():
    '''using local file test if type pdf is io.BufferedReader'''

    pdf_loc = '../pdf2textbox/src/pdf2textbox/data/Id=MMP15%2F57_5694_5696.pdf'
    pdf = _get_pdf_file(pdf_loc, verbose=False)

    assert isinstance(pdf, io.BufferedReader)
