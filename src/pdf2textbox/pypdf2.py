'''
pdf2textbox.py

:param url1: A URL pointing at a PDF file with 2 columns and a header
:returns: Returns a list containing text items that have been extracted from PDF
:raises PDFTextExtractionNotAllowed
'''
import io
import re
import requests
import PyPDF2


def _get_pdf_file(url=None):
    '''
    Download and return a PDF file using requests.
    '''
    if not url:
        base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'
        url1 = '{}Id=MMP14%2F138|16018|16019'.format(base)

        # Fragezeichen, Ausrufezeichen, 18.400, Dr., 8. Februar
        url2 = '{}Id=MMP16%2F139|14617|14630'.format(base)

        # zahlreiche Unterbrechungen, ein einzelnes Wort ("immer") ohne Kontext
        url3 = '{}Id=MMP16%2F140|14760|14768'.format(base)

        # linke Spalte und rechte Spalte nicht auf der gleichen Höhe
        # --> Abruszat's Rede rechte Spalte mit Sätzen aus linker Spalte
        url4 = '{}Id=MMP15%2F57|5694|5696'.format(base)
        pdf4_loc = './data/Id=MMP15%2F57_5694_5696.pdf'

        # Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
        url5 = '{}Id=MMP16%2F8|368|369'.format(base)
        url = url4

    req = requests.get(url, stream=True)
    print('status_code ', req.status_code)
    print('encoding ', req.encoding)
    print('content-type ', req.headers.get('content-type'))

    #with open('test.pdf', 'wb') as fout:
    #    fout.write(req.raw.read())
    #print(req.raw.read())
    #print(req.content)
    #print(req.text)

    pdf = io.BytesIO(req.content)
    print('type req.content', pdf)
    return pdf


def pypdf2():
    '''
    A wrapper function to organize the steps involved to convert a PDF into text:
        1.  Get the PDF file using a URL
        2.  Organize the text in a dict indicating header and columns
        3.  Stripping the text from unwanted special signs
        4.  Return a dictionary containing the text
    '''

    pdfIO_Obj = _get_pdf_file(url=None)
    pdfReader = PyPDF2.PdfFileReader(pdfIO_Obj)
    #print('dir(pdfReader)')
    #print(dir(pdfReader))
    #print('pdfReader.getFields()')
    #print(pdfReader.getFields())
    #print('pdfReader.documentInfo')
    #print(pdfReader.documentInfo)
    #print('pdfReader.getPage(0)')
    #print(pdfReader.getPage(0))
    #print('pdfReader.getPageLayout()')
    #print(pdfReader.getPageLayout())
    #print(type(pdfReader.getPageLayout()))
    #print('pdfReader.numPages')
    #print(pdfReader.numPages)
    #print('pdfReader.pages')
    #print(pdfReader.pages)
    #print('pdfReader.getOutlines()')
    #print(pdfReader.getOutlines())
    #print(pdfReader.outlines)
    #print('pdfReader.trailer')
    #print(pdfReader.trailer)
    #print('pdfReader.flattenedPages')
    #print(pdfReader.flattenedPages)
    #print('pdfReader.getNamedDestinations()')
    #print(pdfReader.getNamedDestinations())
    #print('pdfReader.getPageMode()')
    #print(pdfReader.getPageMode())

    pageObj = pdfReader.getPage(0)
    print('dir(pageObj)')
    print(dir(pageObj))
    #print('pageObj.items()')
    #print(pageObj.items())
    #print(type(pageObj.items()))
    #print('pageObj.keys()')
    #print(pageObj.keys())
    #print('pageObj.values()')
    #print(pageObj.values())
    #print('pageObj.getObject()')
    #print(pageObj.getObject())
    text_bits = pageObj.extractText().split('\n')
    text = ''
    for i in text_bits:
        text = text.join(i)
    print(text)



if __name__ == '__main__':
    pypdf2()
