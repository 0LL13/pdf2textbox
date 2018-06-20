'''
pdf2textbox.py

:param url1: A URL pointing at a PDF file with max 3 columns and a header
:returns: Returns a dict containing text items that have been extracted from PDF
:raises NameError
:raises UnboundLocalError
:raises PDFTextExtractionNotAllowed
'''
import io
import os
import sys

import requests
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines

from collections import namedtuple
from optparse import OptionParser


def main():
    '''
    A wrapper function to organize the steps involved to convert a PDF into text:
        1.  Get the PDF file using either a URL or a locally stored file location
        2.  Check argument if the PDF will be sliced (i.e. use only part of PDF file)
        3.1 If option --slice: get the start and end page number
        3.2 Determine page layout
        4.  Move text and page parameters into a fitting dictionary
    '''

    parser = OptionParser()
    parser.add_option("-s", "--slice",
                      action="store_true", dest="slice", default=False,
                      help="slice PDF file --> tries to find start and end page")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print additional information to stout")
    (options, args) = parser.parse_args()
    verbose = options.verbose

    pdf_loc = _get_url()
    if not pdf_loc:
        pdf_loc = _get_local_file()

    pdf = _get_pdf_file(pdf_loc, verbose)

    if options.slice:
        page_from, page_to = _get_pages(pdf_loc, verbose)
        boxes = _pdf_to_text_slice(pdf, page_from, page_to, verbose)
        _print_boxes_sliced(boxes, page_from, page_to)
    else:
        boxes = _pdf_to_text_all(pdf, verbose)
        _print_boxes_all(boxes)

    pdf.close()



def _get_url(url=None):
    '''
    Manually choose url.
    If none is chosen, url remains None.
    Returns url.
    '''
    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'
    url1 = '{}Id=MMP14%2F138|16018|16019'.format(base)

    # Fragezeichen, Ausrufezeichen, 18.400, Dr., 8. Februar
    url2 = '{}Id=MMP16%2F139|14617|14630'.format(base)

    # zahlreiche Unterbrechungen, ein einzelnes Wort ("immer") ohne Kontext
    url3 = '{}Id=MMP16%2F140|14760|14768'.format(base)

    # linke Spalte und rechte Spalte nicht auf der gleichen Höhe
    # --> Abruszat's Rede rechte Spalte mit Sätzen aus linker Spalte
    url4 = '{}Id=MMP15%2F57|5694|5696'.format(base)

    # Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
    # Einzelnes Wort ("intensiver") ohne Kontext
    url5 = '{}Id=MMP16%2F8|368|369'.format(base)
    #url = url4

    return url


def _get_local_file():
    '''
    Manually choose file location.
    Since this is the default in case no url is given, assert pdf_loc exists.
    Returns pdf_loc.
    '''
    pdf_loc = './data/three_col_horizontal.pdf'
    pdf_loc = './data/three_col_vertical.pdf'
    #pdf_loc = './data/Id=MMP16%2F139_14622_14624.pdf'  # needs page_from, page_to
    pdf_loc = './data/Id=MMP15%2F57_5694_5696.pdf'

    try:
        assert pdf_loc
    except NameError:
        print('No PDF file given.')
        raise

    return pdf_loc


def _get_pdf_file(pdf_loc, verbose):
    '''
    Either download and return a PDF file using requests or
    check if PDF file location exists and open it.
    Returns pdf.
    '''
    print(pdf_loc)
    if 'http' in pdf_loc:
        url = pdf_loc
        req = requests.get(url, stream=True)
        pdf = io.BytesIO(req.content)
        if verbose:
            print('url:')
            print(' ', url)
            print('status_code:')
            print(' ', req.status_code)
            print('encoding:')
            print(' ', req.encoding)
            print('content-type:')
            print(' ', req.headers.get('content-type'))
            print('type req.content:')
            print(' ', pdf)
    elif os.path.isfile(pdf_loc):
        pdf = open(pdf_loc, 'rb')
        if verbose:
            print(type(pdf))

    try:
        assert pdf
    except UnboundLocalError:
        print('Could not access PDF file.')
        raise

    return pdf


def _get_pages(loc, verbose):
    '''
    Find out if start and end page can be retrieved from filename (loc)
    If not, ask user for start and end page.
    Return page_from, page_to.
    '''

    loc = loc.split('.pdf')[0]
    if _check_page_delimiter(loc):
        if '_' in loc:
            pages = loc.split('_')[-2:]
            page_from = pages[0]
            page_to = pages[-1]
        elif '|' in loc:
            pages = loc.split('|')[-2:]
            page_from = pages[0]
            page_to = pages[-1]
    else:
        page_from = _ask_for_page_to_start_from()
        try:
            if isinstance(int(page_from), int):
                pass
        except ValueError:
            page_from = _ask_for_page_to_start_from()

        page_to = _ask_for_page_to_end_at()
        try:
            if isinstance(int(page_to), int):
                pass
        except ValueError:
            page_to = _ask_for_page_to_end_at()

    if verbose:
        print('Slice from page {} to page {}'.format(page_from, page_to))
        print()
    return page_from, page_to


def _check_page_delimiter(loc):
    if '_' or '|' in loc:
        return True
    else:
        return False


def _ask_for_page_to_start_from():
    page_from = input('Which page to start? ')
    try:
        if isinstance(int(page_from), int):
            return page_from
    except ValueError:
        return _ask_for_page_to_start_from()


def _ask_for_page_to_end_at():
    page_to = input('Which page to end? ')
    try:
        if isinstance(int(page_to), int):
            return page_to
    except ValueError:
        return _ask_for_page_to_end_at()


def _pdf_to_text_slice(pdf, page_from, page_to, verbose):
    '''
    Converts PDF documents with up to three columns into text.
    Will only convert part of a PDF file as indicated by page_from, page_to.
    Determine layout (vertical/horizontal) first.
    Calculate the number of columns:
        - get the width of boxes
        - divide max horizontal width by max box width
          --> nr of columns
    Determine if there is a header. This is done in two steps.
    Create a dictionary organized in pagenumber, header, columns.
    Enter text into dictionary.
    Return dictionary.
    '''
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    if verbose:
        print('document.info:')
        for items in document.info:
            for key, value in items.items():
                print('  {}: {}'.format(key, value))
        print()
        outlines = document.get_outlines()
        print('outlines:')
        for (level,title,dest,a,se) in outlines:
            print('  level:', level)
            print('  title:', title)
            print('  dest:', dest)
            print('  a:', a)
            print('  se:', se)
        print()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    boxes = dict()
    page_nr = index = 0
    VERTICAL = HORIZONTAL = False
    token_start = token_end = False

    for page in PDFPage.create_pages(document):
        page_nr += 1
        interpreter.process_page(page)
        LTPage = device.get_result()
        try:
            if index >= 1:
                index = index + 2
            else:
                index = 1
            if int(page.doc.catalog['PageLabels']['Nums'][index]['St']) ==\
                    int(page_from):
                        token_start = True
            elif int(page.doc.catalog['PageLabels']['Nums'][index]['St']) ==\
                    int(page_to):
                        token_end = True
        except KeyError:
            token_start, token_end = _find_start_and_end_page(LTPage, page_from,\
                    page_to, token_start, token_end)

        if token_start:
            boxes = _fill_boxes(LTPage, VERTICAL, HORIZONTAL, boxes, page_nr)
        if token_end:
            token_start = False
            token_end = False

    return boxes


def _pdf_to_text_all(pdf, verbose):
    '''
    Converts PDF documents with up to three columns into text.
    Will convert the whole document, or die trying.
    Determine layout (vertical/horizontal) first.
    Calculate the number of columns:
        - get the width of boxes
        - divide max horizontal width by max box width
          --> nr of columns
    Determine if there is a header. This is done in two steps.
    Create a dictionary organized in pagenumber, header, columns.
    Enter text into dictionary.
    Return dictionary.
    '''
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    if verbose:
        print('document.info:')
        for items in document.info:
            for key, value in items.items():
                print('  {}: {}'.format(key, value))
        print()
        try:
            outlines = document.get_outlines()
            print('outlines:')
            for (level,title,dest,a,se) in outlines:
                print('  level:', level)
                print('  title:', title)
                print('  dest:', dest)
                print('  a:', a)
                print('  se:', se)
            print()
        except PDFNoOutlines:
            print('No outlines available.')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    boxes = dict()
    page_nr = index = 0
    VERTICAL = HORIZONTAL = False
    token_start = token_end = False

    for page in PDFPage.create_pages(document):
        page_nr += 1
        interpreter.process_page(page)
        LTPage = device.get_result()

        boxes = _fill_boxes(LTPage, VERTICAL, HORIZONTAL, boxes, page_nr)

    return boxes


def _print_boxes_sliced(boxes, page_from, page_to):
    token = False
    for key, value in boxes.items():
        print(key)
        for kk, vv in value.items():
            print(kk)
            for box in vv:
                if token:
                    print('-'*60)
                    print(box.x0, box.x1, box.y0, box.y1)
                    print(box.text)
                elif 'header' in kk:
                    if page_from in box.text:
                        token = True
                        print('-'*60)
                        print(box.x0, box.x1, box.y0, box.y1)
                        print(box.text)
                    elif page_to in box.text:
                        token = False


def _print_boxes_all(boxes):
    for key, value in boxes.items():
        print(key)
        for kk, vv in value.items():
            print(kk)
            for box in vv:
                print('-'*60)
                print(box.x0, box.x1, box.y0, box.y1)
                print(box.text)


def _fill_boxes(LTPage, VERTICAL, HORIZONTAL, boxes, page_nr):
    VERTICAL, HORIZONTAL = _get_page_layout(LTPage, VERTICAL, HORIZONTAL)
    NR_OF_COLS, X0_MIN, X1_MAX, BOX_WIDTH_MAX, Y_HEADER =\
            _get_page_parameters(LTPage)
    boxes[page_nr] = dict()
    boxes = _init_boxes(Y_HEADER, NR_OF_COLS, page_nr, boxes)

    for LTLine in LTPage:
        try:
            text = LTLine.get_text()
        except AttributeError:
            text = None
        x0, x1, y0, y1 = _get_box_borders(LTLine)

        box = namedtuple('box', ['x0', 'x1', 'y0', 'y1', 'text'])
        if y0 >= Y_HEADER:
            boxes[page_nr]['header'].append(box(x0, x1, y0, y1, text))
        elif NR_OF_COLS == 1:
            boxes[page_nr]['column'].append(box(x0, x1, y0, y1, text))
        elif NR_OF_COLS == 2:
            if x0 < (X0_MIN + BOX_WIDTH_MAX):
                boxes[page_nr]['left_column'].append(box(x0, x1, y0, y1, text))
            else:
                boxes[page_nr]['right_column'].append(box(x0, x1, y0, y1, text))
        elif NR_OF_COLS == 3:
            col = _choose_col(x0, x1, X0_MIN, X1_MAX, BOX_WIDTH_MAX)
            boxes[page_nr][col].append(box(x0, x1, y0, y1, text))
        else:
            break

    return boxes


def _get_page_parameters(LTPage):
    BOX_WIDTH_MAX = Y_HEADER = BOX_UPPER_Y = 0
    box_upper_y = list()
    X0_MIN = X1_MAX = Y0_MIN = Y0_MAX = Y1_MAX = 0

    for LTLine in LTPage:
        x0, x1, y0, y1 = _get_box_borders(LTLine)
        X0_MIN = _get_X0_MIN(x0, X0_MIN)
        X1_MAX = _get_X1_MAX(x1, X1_MAX)
        Y0_MIN = _get_Y0_MIN(y0, Y0_MIN)
        Y0_MAX = _get_Y0_MAX(y0, Y0_MAX)
        Y1_MAX = _get_Y1_MAX(y1, Y1_MAX)

        BOX_WIDTH_MAX = _get_box_width(BOX_WIDTH_MAX, Y0_MAX, x0, x1, y0, y1)
        Y_HEADER = _get_y_header(Y_HEADER, x0, x1, y0, y1, Y0_MAX, BOX_WIDTH_MAX)

        if y1 < Y_HEADER:
            box_upper_y.append((y0, y1))

        Y_HEADER = _correct_y_header(box_upper_y, Y_HEADER)

    PAGE_WIDTH = X1_MAX - X0_MIN
    if PAGE_WIDTH > 0:
        NR_OF_COLS = PAGE_WIDTH//BOX_WIDTH_MAX
    else:
        NR_OF_COLS = 0

    return NR_OF_COLS, X0_MIN, X1_MAX, BOX_WIDTH_MAX, Y_HEADER


def _init_boxes(Y_HEADER, NR_OF_COLS, page_nr, boxes):
    if Y_HEADER > 0:
        boxes[page_nr]['header'] = list()
    if NR_OF_COLS == 1:
        boxes[page_nr]['column'] = list()
    elif NR_OF_COLS == 2:
        boxes[page_nr]['left_column'] = list()
        boxes[page_nr]['right_column'] = list()
    elif NR_OF_COLS == 3:
        boxes[page_nr]['left_column'] = list()
        boxes[page_nr]['center_column'] = list()
        boxes[page_nr]['right_column'] = list()
    else:
        for counter in range(NR_OF_COLS):
            col = 'col_{}'.format(counter+1)
            boxes[page_nr][col] = list()

    return boxes


def _get_box_borders(LTLine):
    x0 = LTLine.x0
    x0 = round(x0)
    x1 = LTLine.x1
    x1 = round(x1)
    y0 = LTLine.y0
    y0 = round(y0)
    y1 = LTLine.y1
    y1 = round(y1)

    return x0, x1, y0, y1


def _get_page_layout(LTPage, VERTICAL, HORIZONTAL):
    height = LTPage.height
    width = LTPage.width
    if height > width and not HORIZONTAL:
        VERTICAL = True
    elif height > width and HORIZONTAL:
        print('PDF document mixes horizontal and vertical pages')
        VERTICAL = True
        HORIZONTAL = False
    elif height < width and not VERTICAL:
        HORIZONTAL = True
    elif height < width and VERTICAL:
        print('PDF document mixes horizontal and vertical pages')
        VERTICAL = False
        HORIZONTAL = True
    else:
        print('height and width are same length?')
        print(height, width)

    return VERTICAL, HORIZONTAL


def _get_X0_MIN(x0, X0_MIN):
    if X0_MIN == 0:
        X0_MIN = x0
    else:
        if 0 < x0 < X0_MIN:
            X0_MIN = x0

    return X0_MIN


def _get_X1_MAX(x1, X1_MAX):
    if X1_MAX == 0:
        X1_MAX = x1
    else:
        if x1 > X1_MAX > 0:
            X1_MAX = x1

    return X1_MAX


def _get_Y0_MIN(y0, Y0_MIN):
    if Y0_MIN == 0:
        Y0_MIN = y0
    else:
        if 0 < y0 < Y0_MIN:
            Y0_MIN = y0

    return Y0_MIN


def _get_Y0_MAX(y0, Y0_MAX):
    if Y0_MAX == 0:
        Y0_MAX = y0
    else:
        if y0 > Y0_MAX > 0:
            Y0_MAX = y0

    return Y0_MAX


def _get_Y1_MAX(y1, Y1_MAX):
    if Y1_MAX == 0:
        Y1_MAX = y1
    else:
        if y1 > Y1_MAX > 0:
            Y1_MAX = y1

    return Y1_MAX


def _choose_col(x0, x1, X0_MIN, X1_MAX, BOX_WIDTH_MAX):
    if x0 < (X0_MIN + BOX_WIDTH_MAX):
        col = 'left_column'
    elif x0 > (X0_MIN + BOX_WIDTH_MAX) and x1 < (X1_MAX - BOX_WIDTH_MAX):
        col = 'center_column'
    else:
        col = 'right_column'

    return col


def _get_box_width(BOX_WIDTH_MAX, Y0_MAX, x0, x1, y0, y1):
    if BOX_WIDTH_MAX == 0:
        BOX_WIDTH_MAX = x1 - x0
    elif (x1 - x0) > BOX_WIDTH_MAX and y0 < y1 < Y0_MAX:
        BOX_WIDTH_MAX = x1 - x0

    return BOX_WIDTH_MAX


def _get_y_header(Y_HEADER, x0, x1, y0, y1, Y0_MAX, BOX_WIDTH_MAX):
    if y1 >= Y0_MAX:
        if Y_HEADER == 0:
            Y_HEADER = y0
        elif (x1 - x0) > BOX_WIDTH_MAX:
            Y_HEADER = y0

    return Y_HEADER


def _correct_y_header(box_upper_y, Y_HEADER):
    yise = dict()
    for y in box_upper_y:
        try:
            if yise[y[0]] > 0:
                i = yise[y]
                yise[y] = i+1
        except KeyError:
            yise[y] = 1

    s = [{y: yise[y]} for y in sorted(yise, key=yise.get, reverse=True)]
    if s:
        for key in s[0].keys():
            Y_HEADER = key[-1]

    return Y_HEADER


def _find_start_and_end_page(LTPage, page_from, page_to, token_start, token_end):
    token = True
    if token:
        for LTLine in LTPage:
            try:
                text = LTLine.get_text()
                token = False
                if page_from in text:
                    token_start = True
                    #print(text)
                if page_to in text:
                    token_end = True
            except AttributeError:
                token = True
    if token:
        for LTRect in LTPage:
            try:
                text = LTRect.get_text()
                token = False
                if page_from in text:
                    token_start = True
                    #print(text)
                if page_to in text:
                    token_end = True
            except AttributeError:
                token = True
    if token:
        for LTFigure in LTPage:
            try:
                text = LTFigure.get_text()
                token = False
                if page_from in text:
                    token_start = True
                    #print(text)
                if page_to in text:
                    token_end = True
            except AttributeError:
                token = True
    if token:
        for LTTextBoxHorizontal in LTPage:
            try:
                text = LTTextBoxHorizontal.get_text()
                token = False
                if page_from in text:
                    token_start = True
                    #print(text)
                if page_to in text:
                    token_end = True
            except AttributeError:
                token = True

    return token_start, token_end


if __name__ == '__main__':
    main()
