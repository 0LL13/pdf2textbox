from setuptools import setup, find_packages


setup(
    name = 'pdf2textbox',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    version = '0.1.3',
    description = 'A PDF-to-text converter based on pdfminer2',
    long_description = "The pdf2textbox converter aims at converting PDF that comes\
                        in up to three columns and a header into text without loosing\
                        too much information.\
                        Allows command line parameter -s (--slice) to indicate that\
                        only part of the PDF document is of interest. Start and end\
                        page will then either retreived from the document's name\
                        using either '_' or '|' as delimiters or - if start and end\
                        page cannot be found - user input is requested.",
    author = 'Oliver Stapel',
    author_email = 'hardy.ecc95@gmail.com',
    url = 'https://github.com/0LL13/pdf2textbox',
    download_url = 'https://github.com/0LL13/pdf2textbox/archive/0.1.2.tar.gz',
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

