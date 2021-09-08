from pdfextract.pdf_mining import pdf2dom
from pdfextract.page_creation import domdocument2pages
from pdfextract.xml_util import getChildElementsByTagName
from pdfextract.book_creation import pages2book
from epubmaker.epub_creation import create_epub


#############
#main
#############
FILE = 'testfiles/bachelorarbeit_vorlage-master/Bacherlorarbeit.pdf'

#parse pdf with pdfminer into a xml-dom (string in unicode) and then convert to a dom-tree with minidom
dom= pdf2dom(FILE)

#translate the dom data structure into internal python data structure (pages)
pages = domdocument2pages(dom)

#apply heuristics to the textlines in pages to find their probable type, then convert them into internal data structure compatible to epubs
book = pages2book(pages)

#convert into epub
create_epub(book)
