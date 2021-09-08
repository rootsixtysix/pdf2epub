#from pdfextract.pages import Pages, apply_to_pages
from pdfextract.book import Book
import os

"""
!!!
IMPORTANT: Pandoc needs to be installed on the computer!
!!!
with the use of pandoc an ebook in epub format is created out of an xhtml file
"""

PATH='testfiles/'
TITLE='Masterarbeit'
FILE='book.xhtml'

XHTML_HEAD="""<?xml version="1.0" encoding="ISO-8859-1" ?>
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta http-equiv="content-type" content="text/html" charset="utf-8" />
    <title>Masterarbeit</title>
  </head>
  <body>"""

XHTML_CLOSERS = '</body> </html>'

def create_epub(book):
    book2xhtml(book)
    xhtml2epub()

def book2xhtml(book):
    xhtmlstring = XHTML_HEAD
    for c in book.children():
        xhtmlstring = xhtmlstring + c._to_xhtml()
    xhtmlstring = xhtmlstring + XHTML_CLOSERS
    with open(PATH+FILE, 'w') as fa:
        fa.write(xhtmlstring)

def xhtml2epub(file=FILE, title=TITLE, path=PATH):
    command='pandoc -o '+ path + title + '.epub' + ' ' + path + file
    #command=' pandoc -o testfiles/book.epub testfiles/t'
    os.system(command)
