import io
import os

from src.pdf2textbox.pdf2textbox import _get_pdf_file
from src.pdf2textbox.pdf2textbox import _get_textbox
from src.pdf2textbox.pdf2textbox import _extract_textboxes


def _get_pdf():
    '''get the pdf from chosen urls'''

    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'

    # Fragezeichen, Ausrufezeichen, 18.400, Dr., 8. Februar
    url1 = '{}Id=MMP16%2F139|14617|14630'.format(base)

    # zahlreiche Unterbrechungen, ein einzelnes Wort ("immer") ohne Kontext
    url2 = '{}Id=MMP16%2F140|14760|14768'.format(base)

    # linke Spalte und rechte Spalte nicht auf der gleichen Höhe
    # --> Abruszat's Rede rechte Spalte mit Sätzen aus linker Spalte
    url3 = '{}Id=MMP15%2F57|5694|5696'.format(base)

    # Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
    url4 = '{}Id=MMP16%2F8|368|369'.format(base)

    for url in [url1, url2, url3, url4]:
        pdf = _get_pdf_file(url)
        yield pdf


def test_url(url):
    '''test type textbox is dict'''

    pdf = _get_pdf_file(url)
    pdf = open(file_loc, 'br')
    textbox = _get_textbox(pdf)

    print(textbox)



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


if __name__ == '__main__':
    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'
    url1 = '{}Id=MMP16%2F139|14617|14630'.format(base)
    test(url1)
