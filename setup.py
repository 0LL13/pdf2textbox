from setuptools import setup, find_packages


setup(
    name = 'pdf2textbox',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    version = '0.1.2',
    description = 'A PDF-to-text converter based on pdfminer2',
    long_description = 'The pdf2textbox converter aims at converting PDF that comes\
                        in two columns and a header into text without loosing too\
                        much information. To this end it uses the x0 and y1\
                        coordinates to differentiate between left and right\
                        column and header. Text is then stripped of unwanted\
                        special signs and stored in a dictionary that contains\
                        pagenumber, header, left and right column as found in the\
                        PDF document.',
    author = 'Oliver Stapel',
    author_email = 'hardy.ecc95@gmail.com',
    url = 'https://github.com/0LL13/pdf2textbox',
    download_url = 'https://github.com/0LL13/pdf2textbox/archive/0.1.tar.gz',
    keywords = ['PDF', 'pdfminer2', 'PDF conversion', 'text processing'],
    license='MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        ],
    )

# 'Topic :: Text Processing',
# 'Intended Audience :: PDF scrapers',
# 'Development Status :: 5 - Stable',
