from setuptools import setup, find_packages


setup(
    name = 'pdf2textbox',
    packages=['src/pdf2textbox/'],
    version = '0.2.3',
    description = 'A PDF-to-text converter based on pdfminer2',
    long_description = "The pdf2textbox converter aims at converting PDF with up to\
                        three columns and a header into text without loosing too\
                        much information.\
                        Allows command line parameter -s (--slice) to indicate that\
                        only part of the PDF document is of interest. Start and end\
                        page will then be either retreived from the document's name\
                        using '_' or '|' as delimiters or - if start and end page\
                        cannot be found - user input is requested.",
    author = 'Oliver Stapel',
    author_email = 'hardy.ecc95@gmail.com',
    keywords = ['PDF', 'pdfminer2', 'PDF conversion', 'text processing'],
    license='MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Text Processing :: General',
        'Intended Audience :: Science/Research',
        ],
    )
