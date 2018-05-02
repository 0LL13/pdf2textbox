from distutils.core import setup


setup(
    name = 'pdf2textbox',
    packages = ['pdf2textbox'],
    version = '0.1',
    description = 'A PDF-to-text converter based on pdfminer2',
    author = 'Oliver Stapel',
    author_email = 'hardy.ecc95@gmail.com',
    url = 'https://github.com/0LL13/pdf2textbox',
    download_url = 'https://github.com/0LL13/pdf2textbox/archive/0.1.tar.gz',
    keywords = ['PDF', 'pdfminer2', 'PDF conversion', 'text processing'],
    license='MIT',
    classifiers = [
        'Development Status :: 5 - Stable',
        'Intended Audience :: PDF scrapers',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        ],
    )
