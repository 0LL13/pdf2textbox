'''
pdf2textbox.py

:param url1: A URL pointing at a PDF file with 2 columns and a header
:returns: Returns a list containing text items that have been extracted from PDF
:raises PDFTextExtractionNotAllowed
'''
import io
import re
import requests

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


def _get_pdf_file(url=None):
    '''
    Download and return a PDF file using requests.
    '''
    if not url:
        base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'
        #url1 = '{}Id=MMP14%2F138|16018|16019'.format(base)

        #url2 = 'http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf'
        #url3 = 'http://www.pdf995.com/samples/pdf.pdf'
        #url4 = 'https://www.einfach-fuer-alle.de/download/pdf_barrierefrei.pdf'

        # Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
        url5 = '{}Id=MMP16%2F8|368|369'.format(base)
        url = url5

    req = requests.get(url)
    print('status_code ', req.status_code)
    print('encoding ', req.encoding)
    print('content-type ', req.headers.get('content-type'))

    pdf = io.BytesIO(req.content)
    print('type req.content', pdf)
    return pdf


def pdf2textbox():
    '''
    A wrapper function to organize the steps involved to convert a PDF into text:
        1.  Get the PDF file using a URL
        2.  Organize the text in a dict indicating header and columns
        3.  Stripping the text from unwanted special signs
        4.  Return a dictionary containing the text
    '''
    pdf = _get_pdf_file(url=None)
    textbox_dict = _get_textbox(pdf)
    for key, val in textbox_dict.items():
        for subkey, subval in val.items():
            if 'column' in subkey:
                textbox_dict[key][subkey] = _extract_textboxes(subval)
                #for box in textbox_dict[key][subkey]:
                #    print(box)
            else:
                textbox_dict[key]['header'] = _extract_textboxes(subval)
                tmp_list = list()
                for item in textbox_dict[key]['header']:
                    tmp_list.append(item.rstrip())
                textbox_dict[key]['header'] = tmp_list
                #print(textbox_dict[key]['header'])
            #print()

    return textbox_dict


def _extract_textboxes(textbox_list):
    box_list = list()
    for box in textbox_list:
        if box.endswith(">>"):
            box = box[:-2]
        if box.endswith("'"):
            box = box[:-1]
        box.rstrip()
        if box == '0':
            continue
        box = box[:-2]
        box.rstrip()
        box.lstrip()
        if box.startswith(" '"):
            box = box[2:]
        if box.startswith("00 '"):
            box = box[4:]
        if box.startswith("0 '"):
            box = box[3:]
        box = re.sub(r'(\\n)', '', box)
        box = re.sub(' +', ' ', box)
        if box == ' ':
            continue
        box_list.append(box)

    return box_list


def _get_textbox(pdf):
    '''
    row in rows will be:
        row[0]  page_number
        row[1]  x0
        row[2]  y0
        row[3]  x1
        row[4]  y1
        row[5]  text

    I use page_number, y1, x0 and text.
    y1 indicates if a line is part of the header, this can be adjusted by
    changing parameter HEADER_AT.
    x0 helps decide if a text-bit is left or right column, this can be
    adjusted by changing parameter LEFT_COLUMN_UNTIL.

    Instead of aiming at the lines, I found that the textboxes can be obtained
    by getting the LTLine in LTPage (LTLine not being a line!!) and next
    LTLine.analyze and taking care of the vertikal position (y1) I was able to
    get the text bits in a coherent order and fashion.

    Returns a dictionary organized in page, header, left and right column
    '''
    HEADER_AT = 760
    LEFT_COLUMN_UNTIL = 299
    textbox_dict = dict()
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_counter = 1
    for page in PDFPage.create_pages(document):
        textbox_dict[page_counter] = dict()
        textbox_dict[page_counter]['header'] = list()
        textbox_dict[page_counter]['left_column'] = list()
        textbox_dict[page_counter]['right_column'] = list()
        interpreter.process_page(page)
        LTPage = device.get_result()
        for LTLine in LTPage:
            x0 = LTLine.x0
            x0 = round(x0)
            y1 = LTLine.y1
            y1 = round(y1, 3)
            textbox = str(LTLine.analyze)
            textbox = textbox.split('{}'.format(y1))[-1]
            if int(y1) > HEADER_AT:
                textbox_dict[page_counter]['header'].append(textbox)
            elif int(x0) < LEFT_COLUMN_UNTIL:
                textbox_dict[page_counter]['left_column'].append(textbox)
            else:
                textbox_dict[page_counter]['right_column'].append(textbox)
        page_counter += 1

    #print(textbox_dict)
    return textbox_dict


if __name__ == '__main__':
    text_in_boxes = pdf2textbox()
    print(text_in_boxes)
