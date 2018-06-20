============
pdf2textbox
============

A PDF-to-text converter based on pdfminer2 (which is based on
pdfminer.six which is based on pdfminer).
Converts PDF files with up to 3 columns to text and avoids the
caveats that multi-columned PDF files have in store for PDF
conversion.


Features
--------

Convert PDF to text in the original order. This works well for PDF-files
without tables, graphs, and other stuff.

Note:
The textboxes will rarely be identical with paragraphs of the
PDF-file.
There might be cases when a textbox ends mid-sentence just to be
coninued with the next box. This is due to the PDF file's graphic-
oriented organization of content. However, the order of text will
be correct.

When a document contains tables and other stuff, there is still a good
chance to get hold of the text in a meaningful order, however the task
to strip and reconnect the boxes will become tedious.

Installation
------------

pip install pdf2textbox

Contribute
----------

- Issue Tracker: github.com/0LL13/pdf2textbox/issues
- Source Code: github.com/0LL13/pdf2textbox/src/pdf2textbox

Support
-------

Feel free to fork and improve.

Warranty
--------

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY
DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

License
-------

MIT
