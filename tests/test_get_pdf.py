import io
import os
import re

from pdf2textbox.pdf2textbox import _get_pdf_file


def test_get_url():
    '''urls that can be chosen in _get_url should be valid url addresses'''

    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'

    urls = ['{}Id=MMP14%2F138|16018|16019'.format(base),
            '{}Id=MMP16%2F139|14617|14630'.format(base),
            '{}Id=MMP16%2F140|14760|14768'.format(base),
            '{}Id=MMP15%2F57|5694|5696'.format(base),
            '{}Id=MMP16%2F11|542|544'.format(base)]

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

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_locs = ['{}/Id=MMP16%2F139_14622_14624.pdf'.format(loc),
                '{}/Id=MMP15%2F57_5694_5696.pdf'.format(loc),
                '{}/01a_only_text.pdf'.format(loc),
                '{}/02a_two_cols.pdf'.format(loc),
                '{}/03a_three_cols.pdf'.format(loc),
                '{}/04a_text_and_header.pdf'.format(loc),
                '{}/05a_two_cols_and_header.pdf'.format(loc),
                '{}/06a_three_cols_and_header.pdf'.format(loc)]

    for loc in pdf_locs:
        assert os.path.isfile(loc)


def test_get_pdf_file_url():
    '''using requests test if type pdf is io.BytesIO stream'''

    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'
    url = base + 'Id=MMP16%2F11|542|544'
    print('url', url)
    pdf = _get_pdf_file(url, verbose=False)

    assert isinstance(pdf, io.BytesIO)


def test_get_pdf_file_local():
    '''using local file test if type pdf is io.BufferedReader'''

    cwd = os.getcwd()
    loc = '{}/pdf2textbox/data'.format(cwd)
    pdf_loc = '{}/Id=MMP15%2F57_5694_5696.pdf'.format(loc)

    pdf = _get_pdf_file(pdf_loc, verbose=False)
    assert isinstance(pdf, io.BufferedReader)
