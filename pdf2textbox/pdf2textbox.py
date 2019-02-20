'''
pdf2textbox.py

:param url: A URL pointing at a PDF file with max 3 columns and a header
:returns: Returns a dict containing text items that have been extracted from PDF
:raises NameError
:raises UnboundLocalError
:raises PDFTextExtractionNotAllowed
'''
import io
import os
import requests

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines

from collections import namedtuple
from optparse import OptionParser


def pdf2textbox():
    '''
    A wrapper function to organize the steps involved to convert a PDF doc into text:
        1.  Get the PDF file using either a URL or a locally stored file location
        2.  Check argument if the PDF will be sliced (i.e. use only part of PDF file)
        3.  If option --slice: get the start and end page number
        4.  Move text and page parameters into a fitting dictionary
    '''

    parser = OptionParser()

    parser.add_option("-s", "--slice",
                      action="store_true", dest="slice", default=False,
                      help="slice PDF file --> tries to find start and end page")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print additional information to stout")
    parser.add_option("-l", "--location",
                      action="store", dest="pdf_loc", default=None,
                      help="add url or local address of PDF file")

    (options, args) = parser.parse_args()
    verbose = options.verbose
    pdf_loc = options.pdf_loc

    if not pdf_loc:
        pdf_loc = _get_url()
        if not pdf_loc:
            pdf_loc = _get_local_file()

    pdf = _get_pdf_file(pdf_loc, verbose)

    if options.slice:
        page_from, page_to = _get_pages(pdf_loc, verbose)
        boxes = _pdf_to_text_slice(pdf, page_from, page_to, verbose)
        #_print_boxes_sliced(boxes, page_from, page_to, verbose)
    else:
        boxes = _pdf_to_text_all(pdf, verbose)
        #_print_boxes_all(boxes, verbose)

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
    url5 = '{}Id=MMP16%2F8|542|544'.format(base)
    #url = url4

    # der obere Teil der rechten Spalte wird zu früh wiedergegeben: linke
    # und rechte Spalte werden gemischt
    url6 = '{}Id=MMP14%2F4|175|187'.format(base)

    url7 = '{}Id=MMP14%2F149|17408|17423'.format(base)

    # will miss out first sentence on page 8324 if _fill_boxes has y0 >= Y_HEADER
    # --> changed to y0 > Y_HEADER works
    url8 = '{}Id=MMP14%2F72|8323|8332'.format(base)

    url9 = '{}Id=MMP14%2F149|17408|17423'.format(base)

    # will return empty lists for columns
    url10 = '{}Id=MMP14%2F56|6267|6269'.format(base)

    url = url10
    return url


def _get_local_file():
    '''
    Manually choose file location.
    Since this is the default in case no url is given, assert pdf_loc exists.
    Returns pdf_loc.
    '''
    #pdf_loc = './data/Id=MMP16%2F139_14622_14624.pdf'  # needs page_from, page_to
    #pdf_loc = './data/Id=MMP15%2F57_5694_5696.pdf'
    #pdf_loc = './data/01a_only_text.pdf'
    #pdf_loc = './data/02a_two_cols.pdf'
    #pdf_loc = './data/03a_three_cols.pdf'
    #pdf_loc = './data/04a_text_and_header.pdf'
    #pdf_loc = './data/05a_two_cols_and_header.pdf'
    #pdf_loc = './data/06a_three_cols_and_header.pdf'

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
            print('type pdf:')
            print(' ', type(pdf))
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
        _print_document_info(document)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    boxes = dict()
    page_nr = index = 0
    token_start = token_end = False

    for page in PDFPage.create_pages(document):
        page_nr += 1
        interpreter.process_page(page)
        LTPage = device.get_result()
        try:
            if index >= 1:
                index = index + 2       # why?
            else:
                index = 1               # shouldn't that be 3 ?
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
            boxes = _fill_boxes(LTPage, boxes, page_nr, verbose)
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
        _print_document_info(document)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    boxes = dict()
    page_nr = index = 0
    token_start = token_end = False

    for page in PDFPage.create_pages(document):
        page_nr += 1
        interpreter.process_page(page)
        LTPage = device.get_result()

        boxes = _fill_boxes(LTPage, boxes, page_nr, verbose)

    return boxes


def _print_boxes_sliced(boxes, page_from, page_to, verbose):
    token = False
    for key, value in boxes.items():
        if verbose:
            print(key)
        for kk, vv in value.items():
            if verbose:
                print(kk)
            for box in vv:
                if token:
                    if verbose:
                        print('-'*60)
                        print(box.x0, box.x1, box.y0, box.y1)
                    print(box.text)
                elif 'header' in kk:
                    if page_from in box.text:
                        token = True
                        if verbose:
                            print('-'*60)
                            print(box.x0, box.x1, box.y0, box.y1)
                        print(box.text)
                    elif page_to in box.text:
                        token = False


def _print_boxes_all(boxes, verbose):
    for key, value in boxes.items():
        if verbose:
            print('key (page)', key)
        for kk, vv in value.items():
            if verbose:
                print('part of page:', kk)
            for box in vv:
                if verbose:
                    print('-'*60)
                    print(box.x0, box.x1, box.y0, box.y1)
                print(box.text)


def _fill_boxes(LTPage, boxes, page_nr, verbose):
    NR_OF_COLS, X1_MAX, BOX_WIDTH_MAX, Y_HEADER, UPPER_PAGE_EDGE, SIDE_PAGE_EDGE =\
            _get_page_parameters(LTPage, verbose)
    boxes[page_nr] = dict()
    boxes = _init_boxes(Y_HEADER, UPPER_PAGE_EDGE, NR_OF_COLS, page_nr, boxes)

    for LTLine in LTPage:
        try:
            text = LTLine.get_text()
        except AttributeError:
            text = None
        x0, x1, y0, y1 = _get_box_borders(LTLine)

        box = namedtuple('box', 'x0, x1, y0, y1, text')
        if verbose:
            print('** Deciding which part of the page: header or columns ...')
            print(f'\theader if y0: {y0} >= Y_HEADER: {Y_HEADER}')
        if y0 >= Y_HEADER:
            boxes[page_nr]['header'].append(box(x0, x1, y0, y1, text))
            if verbose:
                print('\t--> header')
                print(text)
        elif NR_OF_COLS == 1:
            boxes[page_nr]['column'].append(box(x0, x1, y0, y1, text))
        elif NR_OF_COLS == 2:
            if verbose:
                print(f'\tif x0: {x0} < {BOX_WIDTH_MAX}, x1: {x1}, y0: {y0}, y1: {y1}')
            if x0 < BOX_WIDTH_MAX:
                boxes[page_nr]['left_column'].append(box(x0, x1, y0, y1, text))
                if verbose:
                    print('\t--> goes to left column')
                    print(text)
            else:
                boxes[page_nr]['right_column'].append(box(x0, x1, y0, y1, text))
                if verbose:
                    print('\t--> goes to right column')
                    print(text)
        elif NR_OF_COLS == 3:
            col = _choose_col(x0, x1, SIDE_PAGE_EDGE, BOX_WIDTH_MAX, verbose)
            boxes[page_nr][col].append(box(x0, x1, y0, y1, text))
        else:
            break

    return boxes


def _get_page_parameters(LTPage, verbose):
    SIDE_PAGE_EDGE = round(LTPage.bbox[2])
    UPPER_PAGE_EDGE = round(LTPage.bbox[3])
    Y_HEADER = UPPER_PAGE_EDGE
    params = namedtuple('params', 'x0, x1, y0, y1, text')
    box_parameters = list()
    X0_MIN = X1_MAX = Y0_MIN = Y0_MAX = Y1_MAX = 0

    for LTLine in LTPage:
        try:
            text = LTLine.get_text()
        except AttributeError:
            text = None
        x0, x1, y0, y1 = _get_box_borders(LTLine)
        X0_MIN = _get_X0_MIN(x0, X0_MIN)
        X1_MAX = _get_X1_MAX(x1, X1_MAX)
        Y0_MIN = _get_Y0_MIN(y0, Y0_MIN)
        Y0_MAX = _get_Y0_MAX(y0, Y0_MAX)
        Y1_MAX = _get_Y1_MAX(y1, Y1_MAX)

        box_parameters.append(params(x0, x1, y0, y1, text))

    Y_HEADER = _get_y_header(UPPER_PAGE_EDGE, box_parameters, Y1_MAX, verbose)
    BOX_WIDTH_MAX = _get_box_width(box_parameters, Y_HEADER)
    PAGE_WIDTH = X1_MAX - X0_MIN

    if PAGE_WIDTH > 0:
        NR_OF_COLS = round(PAGE_WIDTH/BOX_WIDTH_MAX)
    else:
        NR_OF_COLS = 0

    if verbose:
        _print_page_parameters(X0_MIN, X1_MAX, Y0_MIN, Y0_MAX, Y1_MAX,\
                box_parameters, SIDE_PAGE_EDGE, UPPER_PAGE_EDGE,\
                BOX_WIDTH_MAX, Y_HEADER, NR_OF_COLS)

    if _only_one_box(box_parameters, NR_OF_COLS):
        Y_HEADER = UPPER_PAGE_EDGE
    elif _only_one_box(box_parameters, NR_OF_COLS) == None:
        print('Error needs to be defined')
        raise
    else:
        if _all_boxes_aligned(box_parameters, NR_OF_COLS):
            Y_HEADER = UPPER_PAGE_EDGE

    return NR_OF_COLS, X1_MAX, BOX_WIDTH_MAX, Y_HEADER, UPPER_PAGE_EDGE, SIDE_PAGE_EDGE


def _init_boxes(Y_HEADER, UPPER_PAGE_EDGE, NR_OF_COLS, page_nr, boxes):
    if Y_HEADER > 0 and Y_HEADER <= UPPER_PAGE_EDGE:
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
    else:   # more than three columns doesn't make sense, defaulting to two
        boxes[page_nr]['left_column'] = list()
        boxes[page_nr]['right_column'] = list()

    return boxes


def _choose_col(x0, x1, SIDE_PAGE_EDGE, BOX_WIDTH_MAX, verbose):
    if x0 < BOX_WIDTH_MAX and x1 < 2*BOX_WIDTH_MAX:
        col = 'left_column'
    elif x0 > BOX_WIDTH_MAX and x1 < (SIDE_PAGE_EDGE - BOX_WIDTH_MAX):
        col = 'center_column'
    else:
        col = 'right_column'

    if verbose:
        print('x0, x1, BOX_WIDTH_MAX, col')
        print(x0, x1, BOX_WIDTH_MAX, col)
    return col


def _get_box_width(box_parameters, Y_HEADER):
    BOX_WIDTH_MAX = 0
    for params in box_parameters:
        if params.y0 < Y_HEADER:
            if (params.x1 - params.x0) > BOX_WIDTH_MAX:
                if params.y0 < params.y1:
                    BOX_WIDTH_MAX = params.x1 - params.x0

    if BOX_WIDTH_MAX == 0:
        for params in box_parameters:
            if (params.x1 - params.x0) > BOX_WIDTH_MAX:
                BOX_WIDTH_MAX = params.x1 - params.x0

    return BOX_WIDTH_MAX


def _get_y_header(UPPER_PAGE_EDGE, box_parameters, Y1_MAX, verbose):
    '''
    Note: in PDF the upper border of a column can easily be higher than the
    lower boarder of its header (anyway, I'm extrapolating these values).
    --> header text will eventually be in a column, and column text will be found
        inside the header's box ...
    "PDF is evil." (Yusuke Shinyama)
    '''
    headers = list()
    cols = list()
    for params in box_parameters:
        if params.y1 == Y1_MAX:
            headers.append(params)
        else:
            cols.append(params)

    # finding the upper border of columns
    upper_cols_border = 0
    for params in cols:
        if params.y1 > upper_cols_border:
            if params.y1 > params.y0:
                upper_cols_border = params.y1

    # finding the lower border of headers
    y0 = 0
    for params in headers:
        if params.y0 < upper_cols_border:
            if params.y0 > y0:
                y0 = params.y0
        else:
            y0 = upper_cols_border
    Y_HEADER = y0

    return Y_HEADER


def _only_one_box(box_parameters, NR_OF_COLS):
    if len(box_parameters) == NR_OF_COLS:
        x0 = x1 = 0
        y1 = 0
        for params in box_parameters:
            if x1 == 0:
                x0 = params.x0
                x1 = params.x1
                y1 = params.y1
            else:
                if x0 == params.x0 and x1 == params.x1:
                    pass
                elif y1 == params.y1:
                    pass
                else:
                    return False
        return True
    elif len(box_parameters) == 1:
        return True
    elif len(box_parameters) > 1:
        return False
    else:
        print('page without columns')
        raise
        return None


def _all_boxes_aligned(box_parameters, NR_OF_COLS):
    x0 = x1 = None
    y1 = None
    if len(box_parameters) > NR_OF_COLS:           # vertical alignment
        for params in box_parameters:
            if x0 == x1 == None:
                x0 = params.x0
                x1 = params.x1
            else:
                if x0 == params.x0 and x1 == params.x1:
                    pass
                else:
                    return False

    elif len(box_parameters) <= NR_OF_COLS:        # horizontal alignment
        for params in box_parameters:
            if y1 == None:
                y1 = params.y1
            else:
                if y1 == params.y1:
                    pass
                else:
                    return False
    return True


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


def _print_page_parameters(X0_MIN, X1_MAX, Y0_MIN, Y0_MAX, Y1_MAX,\
        box_parameters, SIDE_PAGE_EDGE, UPPER_PAGE_EDGE, BOX_WIDTH_MAX,\
        Y_HEADER, NR_OF_COLS):
    print('*'*60)
    print('X0_MIN', X0_MIN)
    print('X1_MAX', X1_MAX)
    print('Y0_MIN', Y0_MIN)
    print('Y0_MAX', Y0_MAX)
    print('Y1_MAX', Y1_MAX)
    #print(box_parameters)
    print('page edges', SIDE_PAGE_EDGE, UPPER_PAGE_EDGE)
    print('BOX_WIDTH_MAX', BOX_WIDTH_MAX)
    print('Y_HEADER', Y_HEADER)
    print('UPPER_PAGE_EDGE', UPPER_PAGE_EDGE)
    print('NR_OF_COLS', NR_OF_COLS)
    print('*'*60)
    print()


def _print_document_info(document):
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
    except TypeError:
        print('You should change utils.py, line 271, from ord(c) to c')
        print('See also: https://stackoverflow.com/a/19897878/6597765')


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


if __name__ == '__main__':
    pdf2textbox()
