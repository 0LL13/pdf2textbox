'''
pdf2textbox.py

:param url1: A URL pointing at a PDF file with 2 columns and a header
:returns: Returns a list containing text items that have been extracted from PDF
:raises keyError: No
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


def get_pdf_file(url=None):
    '''
    Download and return a PDF file using requests.
    '''
    if not url:
        #url1 = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?Id=MMP14%2F138|16018|16019'

        #url2 = 'http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf'
        #url3 = 'http://www.pdf995.com/samples/pdf.pdf'
        #url4 = 'https://www.einfach-fuer-alle.de/download/pdf_barrierefrei.pdf'

        # Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
        url5 = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?Id=MMP16%2F8|368|369'

        # zahlreiche Unterbrechungen, ein einzelnes Wort ("immer") ohne Kontext:
        #base = './scraper_data/pdf/WP16/ABEL_MARTIN-SEBASTIAN/Id=MMP16%2F140|14762|14764.pdf'

        # Fragezeichen, Ausrufezeichen, 18.400, Dr., 8. Februar:
        #base = './scraper_data/pdf/WP16/ABEL_MARTIN-SEBASTIAN/Id=MMP16%2F139|14622|14624.pdf'

        # Drei Vornamen:
        #base = './scraper_data/pdf/WP15/ZIMKEIT_STEFAN HANS WALTER/Id=MMP15%2F9|583|584.pdf'


    req = requests.get(url5)
    print('status_code ', req.status_code)
    print('encoding ', req.encoding)
    print('content-type ', req.headers.get('content-type'))

    pdf = io.BytesIO(req.content)
    print('type pdf', type(pdf))

    return pdf


def pdf2textbox(pdf):
    '''
    A PDF-to-text converter based on pdfminer2.
    Converts PDF-files to text and avoids the caveats that multi-columned
    PDF-files have in store for the unsuspecting PDF converter.
    Instead of going for the lines, I found that leaving the textboxes intact
    was increasing the chance to get the text in a coherent order.
    This works well for PDF-files without tables, graphs, and other stuff.
    After extracting the text in boxes, there still has to be run another
    function to strip the text of special signs, zeroes and the like.
    Note:   The textboxes will NOT be identical with paragraphs of the PDF-file.
            There might be cases when a textbox ends mid-sentence just to be
            coninued with the next box. This is due to the PDF file's graphic-
            oriented organization of content. However, the order of text will
            be correct.

    When a document contains tables and other stuff, there is still a good
    chance to get hold of the text in a meaningful order, however the task
    of the function to strip and reconnect the boxes will become tedious.

    Receives a buffered bytes stream containing a PDF-file (f).
    Converts pages into a list of textboxes. These boxes contain text.
    Returns a list of texts.
    '''

    textbox_list = list()
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        LTPage = device.get_result()
        #print('LTPage', LTPage)
        for LTLine in LTPage:
            y1 = LTLine.y1
            y1 = round(y1, 3)
            textbox = str(LTLine.analyze)
            textbox = textbox.split('{}'.format(y1))[-1]
            textbox_list.append(textbox)

    return textbox_list


def extract_textboxes(textbox_list):
    '''
    The list of text pieces is reduced of special signs, zeros, and unnecessary
    line breaks. Also words that had to be seperated because EOL was reached can
    get reattached again without heavy use of NLP.

    Receives a list of texts containing all sorts of special characters from the
    PDF document.
    Returns a list of texts that is stripped off those special characters.
    '''
    box_list = list()
    for box in textbox_list:
        if box == '.000>>':
            continue
        if box == '>>':
            continue
        if box == '0':
            continue
        if box.startswith("00 matrix=["):
            continue
        if box.startswith(" matrix=["):
            continue
        if box.startswith("00 '"):
            box = box[4:]
        if box.startswith("0 '"):
            box = box[3:]
        if box.startswith(" '"):
            box = box[2:]
        if box.endswith(">>"):
            box = box[:-2]
        if box.endswith("'"):
            box = box[:-1]
        if box.endswith('"'):
            box = box[:-1]
        box.rstrip()
        box = box[:-2]
        box.rstrip()
        box.lstrip()
        box = re.sub(r'(-\\n)', '', box)
        box = re.sub(r'(\\n)', ' ', box)
        box = re.sub(r'(\\t)', ' ', box)
        if box.lstrip().startswith('(') and box.rstrip().endswith(')'):
            pass
        box = re.sub(' +', ' ', box)
        box_list.append(box)

    return box_list


def main():
    '''Wrapping the module in main()'''

    token = False
    pdf = get_pdf_file(url=None)
    textbox_list = pdf2textbox(pdf)
    box_list = extract_textboxes(textbox_list)

    if box_list:
        token = True
        for box in box_list:
            print(box)
            #print('--'*30)

    return token


if __name__ == '__main__':
    main()
