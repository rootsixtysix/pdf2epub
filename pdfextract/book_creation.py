from pdfextract.page_creation import Page, TextLineType, apply_to_pages, primary, dict_to_sorted_list
import re



"""
This class provides a data structure for the Type Book.
A Book has children elements compatible to xhtml for further processing.
The book has a Node element called Book. This element has all the other elements e.g paragraphs and headings as direct children
So the data structure has only two levels and is quite flat.
Each children includes his text and type.
For further processing (conversion to epub) each child has a function called _to_xhtml()
"""
####################################
# super class for all elements
####################################
class Element:
    def __init__(self, text="", pagenr="", parent=None, children=[]):
        """Initializer.
        Args:
            text:     text in unicode
            pagenr:   Page number of the textbox in the original document
            parent:   Parent node
            children: List of child nodes
        """
        self.text = text
        self.pagenr = pagenr
        self._children = list(children)
        self.id = ""
        for c in self._children:
            c._parent = self

    def children(self):
        return self._children

    def add_child(self, child):
        if child:
            self._children.append(child)
            child._parent = self

    def remove_child(self, child):
        if child in self._children:
            self._children.remove(child)
            child._parent = None

########################################
# Roots and Branche-Elements
########################################
class Book(Element):
    def __init__(self, text="", pagenr="", parent=None, children=[]):
        super(Book, self).__init__(text, pagenr, parent, )


#########################################
# Leafs
########################################
class Paragraph(Element):
    def __init__(self, text='', pagenr=''):
        super(Paragraph, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<p> \n' + self.text + '\n </p> \n'
        return xhtmlstring

class Heading1(Element):
    def __init__(self, text="", pagenr=""):
        super(Heading1, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<h1> \n' + self.text + '\n </h1> \n'
        return xhtmlstring

class Heading2(Element):
    def __init__(self, text="", pagenr=""):
        super(Heading2, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<h2> \n' + self.text + '\n </h2> \n'
        return xhtmlstring

class Heading3(Element):
    def __init__(self, text="", pagenr=""):
        super(Heading3, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<h3> \n' + self.text + '\n </h3> \n'
        return xhtmlstring

class HeadingN(Element):
    def __init__(self, text="", pagenr=""):
        super(HeadingN, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<h4> \n' + self.text + '\n </h4> \n'
        return xhtmlstring

class FigureLabel(Element):
    def __init__(self, text="", pagenr=""):
        super(FigureLabel, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<p> \n' + '<i>' + self.text + '</i>''\n </p> \n'
        return xhtmlstring

class ListOrdered(Element):
    def __init__(self, text="", pagenr=""):
        super(ListOrdered, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<ol> \n' + self.text + '</ol> \n'
        return xhtmlstring

class ListUnordered(Element):
    def __init__(self, text="", pagenr=""):
        super(ListUnordered, self).__init__(text, pagenr)

    def _to_xhtml(self):
        xhtmlstring = '<ul> \n' + self.text + '</ul> \n'
        return xhtmlstring

"""TODO: Test Lists """



"""
HEURISTICS
"""

class HeuristicRegExes:
    SECTION_NR = r"(\.\s?)*(\d\.?)+"
    _WHITE = "[\\s\xa0]"
    _NOT_WHITE = "[^\\s\xa0]"
    _FLOAT_NR = _WHITE + r"*" + SECTION_NR + r":?"

    HEADING_NUMBERED = "[\\d.]*" + _WHITE
    HEADING1_NUMBERED = r"\d[.]?"+ _WHITE + r"\w"              #dezimal+optionaler_punkt+whitespace+alphanummeric
    HEADING2_NUMBERED = r"\d[.]\d[.]?"+ _WHITE + r"\w"
    HEADING3_NUMBERED = r"\d[.]\d[.]\d[.]?"+ _WHITE + r"\w"
    PAGE_NR = r"\d+"

    FIGURE_LABEL = r"((Abbildung)|(Abb\.?)|(Figur)|(Fig\.?)|(Grafik)|(Bild))" + _FLOAT_NR
    TABLE_CAP = r"((Tabelle)|(Tab\.?))" + _FLOAT_NR
    LISTING_CAP = r"((Quelltext)|(Sourcecode)|(Source [Cc]ode))" + _FLOAT_NR
    DEFINITION_CAP = r"((Definition)|(Def\.?))" + _FLOAT_NR
    FORMULA_CAP = r"((Formel))" + _FLOAT_NR
    THEOREM_CAP = r"((Theorem)|(Satz))" + _FLOAT_NR
    PROOF_CAP = r"((Beweis))" + _FLOAT_NR

##########################
# main Function
###########################
def pages2book(pages):
    apply_to_pages(pages, simple_heuristics)
    apply_to_pages(pages, process_simple_heuristics)
    print(pages.heading1.fonts)
    print(pages.heading1.sizes)
    print(pages.heading1.prim_font)
    apply_to_pages(pages, advanced_heuristics)
    book = build_book(pages)
    return book

##################################
# Heuristic Functions
##################################
def simple_heuristics(textbox, page, pages):
    for tl in textbox.textlines:
        regex_heuristics(tl)
        font_heuristics(tl, textbox, page, pages)
        content_and_layout_heuristics(tl, textbox, page, pages)

def process_simple_heuristics(textbox, page, pages):
    for tl in textbox.textlines:
        if tl.probable_type.most_probable() == TextLineType.HEADING1_NUMBERED:
            pages.heading1.add_font(tl.prim_font)
            pages.heading1.add_size(tl.prim_size)
            pages.heading1.prim_font = primary(dict_to_sorted_list(pages.heading1.fonts))
            pages.heading1.prim_size = primary(dict_to_sorted_list(pages.heading1.sizes))
        if tl.probable_type.most_probable() == TextLineType.HEADING2_NUMBERED:
            pages.heading2.add_font(tl.prim_font)
            pages.heading2.add_size(tl.prim_size)
            pages.heading2.prim_font = primary(dict_to_sorted_list(pages.heading2.fonts))
            pages.heading2.prim_size = primary(dict_to_sorted_list(pages.heading2.sizes))
        if tl.probable_type.most_probable() == TextLineType.HEADING3_NUMBERED:
            pages.heading3.add_font(tl.prim_font)
            pages.heading3.add_size(tl.prim_size)
            pages.heading3.prim_font = primary(dict_to_sorted_list(pages.heading3.fonts))
            pages.heading3.prim_size = primary(dict_to_sorted_list(pages.heading3.sizes))

def advanced_heuristics(textbox, page, pages):
    for tl in textbox.textlines:
        advanced_font_heuristics(tl, textbox, page, pages)


class HeuristicRegExes:
    SECTION_NR = r"(\.\s?)*(\d\.?)+"
    _WHITE = "[\\s\xa0]"
    _NOT_WHITE = "[^\\s\xa0]"
    _FLOAT_NR = _WHITE + r"*" + SECTION_NR + r":?"

    HEADING_NUMBERED = "[\\d.]*" + _WHITE
    HEADING1_NUMBERED = r"\d[.]?"+ _WHITE + r"\w"              #dezimal+optionaler_punkt+whitespace+alphanummeric
    HEADING2_NUMBERED = r"\d[.]\d[.]?"+ _WHITE + r"\w"
    HEADING3_NUMBERED = r"\d[.]\d[.]\d[.]?"+ _WHITE + r"\w"
    PAGE_NR = r"\d+"
    FIGURE_LABEL = r"((Abbildung)|(Abb\.?)|(Figur)|(Fig\.?)|(Grafik)|(Bild))" + _FLOAT_NR
    TABLE_LABEL = r"((Tabelle)|(Tab\.?))" + _FLOAT_NR
    LISTING_LABEL = r"((Listing)|(Quelltext)|(Sourcecode)|(Source [Cc]ode))" + _FLOAT_NR

    DEFINITION_CAP = r"((Definition)|(Def\.?))" + _FLOAT_NR
    FORMULA_CAP = r"((Formel))" + _FLOAT_NR
    THEOREM_CAP = r"((Theorem)|(Satz))" + _FLOAT_NR
    PROOF_CAP = r"((Beweis))" + _FLOAT_NR

def regex_heuristics(textline):
    if re.match(HeuristicRegExes.HEADING1_NUMBERED, textline.text):
        textline.probable_type.score[TextLineType.HEADING1_NUMBERED] += 50
    if re.match(HeuristicRegExes.HEADING2_NUMBERED, textline.text):
        textline.probable_type.score[TextLineType.HEADING2_NUMBERED] += 50
    if re.match(HeuristicRegExes.HEADING3_NUMBERED, textline.text):
        textline.probable_type.score[TextLineType.HEADING3_NUMBERED] += 50
    if re.match(HeuristicRegExes.HEADING_NUMBERED, textline.text):
        textline.probable_type.score[TextLineType.HEADING_N_NUMBERED] += 40
    if re.match(HeuristicRegExes.FIGURE_LABEL, textline.text):
        textline.probable_type.score[TextLineType.FIGURE_LABEL] += 50
    if re.match(HeuristicRegExes.TABLE_LABEL, textline.text):
        textline.probable_type.score[TextLineType.TABLE_LABEL] += 50
    if re.match(HeuristicRegExes.LISTING_LABEL, textline.text):
        textline.probable_type.score[TextLineType.LISTING_LABEL] += 50


    if re.match(HeuristicRegExes.PAGE_NR, textline.text):
        textline.probable_type.score[TextLineType.PAGE_NR] += 50


def font_heuristics(textline, textbox, page, pages):
    #check fontsize
    if textline.prim_size > pages.prim_size:
        textline.probable_type.score[TextLineType.HEADING1_NUMBERED] += 30
        textline.probable_type.score[TextLineType.HEADING2_NUMBERED] += 30
        textline.probable_type.score[TextLineType.HEADING3_NUMBERED] += 30
        textline.probable_type.score[TextLineType.HEADING_N_NUMBERED] += 30
        textline.probable_type.score[TextLineType.HEADING1_UNNUMBERED] += 40
        textline.probable_type.score[TextLineType.HEADING2_UNNUMBERED] += 40
        textline.probable_type.score[TextLineType.HEADING3_UNNUMBERED] += 40
    # kleiner
        #footnote, page_nr?, footert
    if textline.prim_size==pages.prim_size and textline.prim_font==pages.prim_font:
        textline.probable_type.score[TextLineType.PARAGRAPH] += 50

    if re.search('italic', textline.prim_font):
        textline.probable_type.score[TextLineType.FIGURE_LABEL] += 20
        textline.probable_type.score[TextLineType.TABLE_LABEL] += 20
        textline.probable_type.score[TextLineType.LISTING_LABEL] += 20

    #wenn größte schrit, dann titel

def content_and_layout_heuristics(textline, textbox, page, pages):
    #line count
    if textbox.line_count == 1:
        textline.probable_type.score[TextLineType.HEADING1_NUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING2_NUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING3_NUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING_N_NUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING1_UNNUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING2_UNNUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING3_UNNUMBERED] += 15
        textline.probable_type.score[TextLineType.HEADING_N_UNNUMBERED] += 15
        textline.probable_type.score[TextLineType.PAGE_NR] += 10

        #PAGE_NR, title, table
    #elif textbox.line_count>1 and textbox.line_count<4:
    #fig
    if textbox.line_count<=3:
        textline.probable_type.score[TextLineType.FIGURE_LABEL] += 15
        textline.probable_type.score[TextLineType.TABLE_LABEL] += 15
        textline.probable_type.score[TextLineType.LISTING_LABEL] += 15
    if textbox.line_count>=3:
        textline.probable_type.score[TextLineType.PARAGRAPH] += 20

    #word_count
    if textbox.word_count <=1:
        textline.probable_type.score[TextLineType.PAGE_NR] += 10
    if textbox.word_count > 1 and textbox.word_count < 10:
        textline.probable_type.score[TextLineType.HEADING1_NUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING2_NUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING3_NUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING_N_NUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING1_UNNUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING2_UNNUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING3_UNNUMBERED] += 5
        textline.probable_type.score[TextLineType.HEADING_N_UNNUMBERED] += 5
    if textbox.word_count > 20:
        textline.probable_type.score[TextLineType.PARAGRAPH] += 10

    #textbox width
    if textbox.width()/page.width() > 0.7:
        textline.probable_type.score[TextLineType.PARAGRAPH] += 20
    if textbox.width()/page.width() < 0.6:
        textline.probable_type.score[TextLineType.FIGURE_LABEL] += 15
        textline.probable_type.score[TextLineType.TABLE_LABEL] += 15
        textline.probable_type.score[TextLineType.LISTING_LABEL] += 15
    if textbox.width()/page.width() < 0.2:
        textline.probable_type.score[TextLineType.PAGE_NR] += 30

    #position
    if textbox.top < 200:                                      #page height is 841.89, ground is 0.0
        textline.probable_type.score[TextLineType.PAGE_NR] += 20

def advanced_font_heuristics(textline, textbox, page, pages):
    if not re.match(HeuristicRegExes.HEADING_NUMBERED, textline.text):
        if textline.prim_size == pages.heading1.prim_size and textline.prim_font == pages.heading1.prim_font:
            textline.probable_type.score[TextLineType.HEADING1_UNNUMBERED] += 40
        if textline.prim_size == pages.heading2.prim_size and textline.prim_font == pages.heading2.prim_font:
            textline.probable_type.score[TextLineType.HEADING2_UNNUMBERED] += 40
        if textline.prim_size == pages.heading3.prim_size and textline.prim_font == pages.heading3.prim_font:
            textline.probable_type.score[TextLineType.HEADING3_UNNUMBERED] += 40


###################################
# build Book Functions
#####################################
def build_book(pages):
    book = Book()
    #node = root
    for page in pages.pages:
        pagenr = page.ID
        for tb in page.textboxes:
            last_line_type = tb.textlines[0].probable_type.most_probable()
            textlines_for_bookelement = []
            for tl in tb.textlines:
                print(tl.text)
                current_line_type = tl.probable_type.most_probable()
                if current_line_type == last_line_type:
                    textlines_for_bookelement.append(tl)
                else:
                    append_to_book(textlines_for_bookelement, pagenr, book)
                    textlines_for_bookelement.clear()
                    last_line_type = current_line_type
            append_to_book(textlines_for_bookelement, pagenr, book)
    return book

def append_to_book(tl_to_append, pagenr, book):
    #initialise
    element = None
    text=''
    if len(tl_to_append)>0:
        type = tl_to_append[0].probable_type.most_probable()
    else:
        type = None

    #check for type and make element
    if type == TextLineType.HEADING1_NUMBERED or type ==TextLineType.HEADING1_UNNUMBERED:
        for tl in tl_to_append:
            text = text + tl.text.strip()
        element = Heading1(text=text, pagenr=pagenr)

    if type == TextLineType.HEADING2_NUMBERED or type ==TextLineType.HEADING2_UNNUMBERED:
        for tl in tl_to_append:
            text = text + tl.text.strip()
        element = Heading2(text=text, pagenr=pagenr)

    if type == TextLineType.HEADING3_NUMBERED or type ==TextLineType.HEADING3_UNNUMBERED:
        for tl in tl_to_append:
            text = text + tl.text.strip()
        element = Heading(text=text, pagenr=pagenr)

    if type == TextLineType.HEADING_N_NUMBERED or type ==TextLineType.HEADING_N_UNNUMBERED:
        for tl in tl_to_append:
            text = text + tl.text.strip()
        element = HeadingN(text=text, pagenr=pagenr)

    if type == TextLineType.PARAGRAPH:
        for tl in tl_to_append:
            text = text + tl.text.strip()
        element = Paragraph(text=text, pagenr=pagenr)

    if type == TextLineType.FIGURE_LABEL or type == TextLineType.TABLE_LABEL or type == TextLineType.LISTING_LABEL:
        for tl in tl_to_append:
            text = text + tl.text.strip()
        element = FigureLabel(text=text, pagenr=pagenr)


    if element!=None:
        book.add_child(element)
