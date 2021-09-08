from pdfextract.xml_util import getChildElementsByTagName

"""
This class provides the architecture for the dom structure, saved as an internal data type called Pages.
Alle Elements include their child elements, some text and information about font and size.
Additionally there are some functions to convert the dom into pages and some analye functions.

ARCHITECTURE:
pages
|
page
|
textgroup
|
TextBox
|
TextLine

Pages is a list of Page Elements.
A Page is a collection of textboxes and textgroups.
A Textgroup is a collection of Textboxes and other textgroups.
Textgroups have hints referring to what TextBoxType is probable
"""

class Pages():
    def __init__(self, pages):
        self.pages = pages
        self.page_count = len(pages)
        self.line_count = 0
        self.word_count = 0
        self.char_count = 0
        self.fonts = dict()
        self.sizes = dict()
        self._init_from_child_pages()
        self.font_count = len(self.fonts)
        self.size_count = len(self.sizes)
        self.prim_font = primary(dict_to_sorted_list(self.fonts))
        self.prim_size = primary(dict_to_sorted_list(self.sizes))
        self.heading1 =  Heading()
        self.heading2 =  Heading()
        self.heading3 =  Heading()

    def _init_from_child_pages(self):
        if self.pages!=[] and self.pages!=None:
            try:
                for p in self.pages:
                    self.line_count += p.line_count
                    self.word_count += p.word_count
                    self.char_count += p.char_count
                    self.fonts = merge_dicts(self.fonts, p.fonts)
                    self.sizes = merge_dicts(self.sizes, p.sizes)
            except:
                print("not all values could be calculated from page information in pages")

class Heading:
    def __init__(self):
        self.fonts = dict()
        self.sizes = dict()
        self.prim_font = ''
        self.prim_size = ''

    def add_font(self, font):
        if font not in self.fonts:
            self.fonts[font] = 1
        else:
            self.fonts[font] += 1

    def add_size(self, size):
        if size not in self.sizes:
            self.sizes[size] = 1
        else:
            self.sizes[size] += 1



class BBox:
    """
    Super class for all objects that have a bounding box (and text).
    """
    def __init__(self, bbox_parameters):
        self.left = bbox_parameters[0]
        self.top = bbox_parameters[1]
        self.right = bbox_parameters[2]
        self.bottom = bbox_parameters[3]

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

class Page(BBox):
    """A page is a collection of textboxes and textgroups."""
    def __init__(self, ID, bbox_parameters, textboxes, textgroups):
        super(Page, self).__init__(bbox_parameters)
        self.ID = ID
        self.textboxes = textboxes
        self._textboxes_by_ID = dict()
        for tb in textboxes:
            self._textboxes_by_ID[tb.ID] = tb
        self.textgroups = textgroups
        self.textbox_count = len(self.textboxes)
        self.textgroup_count = len(self.textboxes)
        self.line_count = 0
        self.word_count = 0
        self.char_count = 0
        self.fonts = dict()
        self.sizes = dict()
        self._init_from_child_textboxes()
        self._init_from_child_textgroups()
        self.font_count = len(self.fonts)
        self.size_count = len(self.sizes)
        self.prim_font = primary(dict_to_sorted_list(self.fonts))
        self.prim_size = primary(dict_to_sorted_list(self.sizes))

    def _init_from_child_textboxes(self):
        if self.textboxes!=[] and self.textboxes!=None:
            try:
                for tb in self.textboxes:
                    self.line_count += tb.line_count
                    self.word_count += tb.word_count
                    self.char_count += tb.char_count
                    self.fonts = merge_dicts(self.fonts, tb.fonts)
                    self.sizes = merge_dicts(self.sizes, tb.sizes)
            except:
                print("not all values could be calculated from textbox information in page")

    def _init_from_child_textgroups(self):
        if self.textgroups!=[] and self.textgroups!=None:
            try:
                for tg in self.textgroups:
                    self.line_count += tb.line_count
                    self.word_count += tb.word_count
                    self.char_count += tb.char_count
                    self.fonts = merge_dicts(self.fonts, tb.fonts)
                    self.sizes = merge_dicts(self.sizes, tb.sizes)
            except:
                print("not all values could be calculated from textgroup information in page")




class TextGroup(BBox):
    def __init__(self, ID, bbox_parameters, Textboxes, textgroups=None):
        super(Textgroup, self).__init__(bbox_parameters)
        self.ID = ID
        self.textboxes = textboxes
        self.textgoups = textgroups
        self.textbox_count = len(self.textboxes)
        self.textgroup_count = len(self.textboxes)
        self.line_count = 0
        self.word_count = 0
        self.char_count = 0
        self.fonts = dict()
        self.sizes = dict()
        self._init_from_child_textboxes()
        self._init_from_child_textgroups()
        self.font_count = len(self.fonts)
        self.size_count = len(self.sizes)
        self.prim_font = primary(dict_to_sorted_list(self.fonts))
        self.prim_size = primary(dict_to_sorted_list(self.sizes))

    def _init_from_child_textboxes(self):
        try:
            for tb in self.textboxes:
                self.line_count += tb.line_count
                self.word_count += tb.word_count
                self.char_count += tb.char_count
                self.fonts = merge_dicts(self.fonts, tb.fonts)
                self.sizes = merge_dicts(self.sizes, tb.sizes)
        except:
            print("not all values could be calculated from textbox information in textgroup")

    def _init_from_child_textgroups(self):
        try:
            for tg in self.textgroups:
                self.line_count += tb.line_count
                self.word_count += tb.word_count
                self.char_count += tb.char_count
                self.fonts = merge_dicts(self.fonts, tb.fonts)
                self.sizes = merge_dicts(self.sizes, tb.sizes)
        except:
            print("not all values could be calculated from textgroup information in textgroup")

class TextBox(BBox):
    def __init__(self, ID, bbox_parameters, textlines):
        super(TextBox, self).__init__(bbox_parameters)
        self.ID = ID
        self.textlines = textlines
        self.line_count = len(textlines)
        self.word_count = 0
        self.char_count = 0
        self.max_chars_per_line = 0
        self.fonts = dict()
        self.sizes = dict()
        #try to calculate following information depeending from children Elements textlines
        self._init_from_child_textlines()
        self.avg_chars_per_line = self.char_count / self.line_count
        self.font_count = len(self.fonts)
        self.size_count = len(self.sizes)
        self.prim_font = primary(dict_to_sorted_list(self.fonts))
        self.prim_size = primary(dict_to_sorted_list(self.sizes))
        #self.probable_type = ProbableTextLineTypes()

    def _init_from_child_textlines(self):
        try:
            for tl in self.textlines:
                self.word_count += tl.word_count
                self.char_count += tl.char_count
                if tl.char_count > self.max_chars_per_line:
                    self.max_chars_per_line = tl.char_count
                self.fonts = merge_dicts(self.fonts, tl.fonts)
                self.sizes = merge_dicts(self.sizes, tl.sizes)
        except:
            print('not all information could be calculated from textlines in Textbox')


class TextLine(BBox):
    """word list is a list of Word() objects"""
    def __init__(self, bbox_parameters, text='', wordlist=[]):
        super(TextLine, self).__init__(bbox_parameters)
        self.text = text
        self.wordlist = wordlist
        self.char_count = len(self.text)
        self.word_count = len(self.wordlist)
        self.avg_word_length = self.char_count / self.word_count
        self.fonts = font_count(self.wordlist)   #dictionary
        self.sizes = size_count(self.wordlist)   #dictionary
        self.font_count = len(self.fonts)
        self.size_count = len(self.sizes)
        self.prim_font = primary(dict_to_sorted_list(self.fonts))
        self.prim_size = primary(dict_to_sorted_list(self.sizes))
        self.probable_type = ProbableTextLineTypes()

class Word:
    def __init__(self):
        self.string = ''
        self.font = None
        self.size = None
        self.color = None


class Letter:
    def __init__(self, char, font, size, color):
        self.char = char
        self.font = font
        self.size = size
        self.color = color

############################################
# Function with a function as parameter, to apply that passed function to all textboxes of the pages
##############################################
def apply_to_pages(pages, function):
    if pages.pages!=[] and pages.pages!=None:
        for page in pages.pages:
            apply_to_page(page, pages, function)

def apply_to_page(page, pages, function):
    if page.textgroups!=[] and page.textgroups!=None:
        for tg in page.textgroups:
            apply_to_textgroup(tg, page, pages, function)
    if page.textboxes!=[] and page.textboxes!=None:
        for tb in page.textboxes:
            apply_to_textbox(tb, page, pages, function)

def apply_to_textgroup(textgroup, page, pages, function):
    if textgroup.textgroups!=[] and textgroup.textgroups!=None:
        for tg in textgroup.textgroups:
            apply_to_textgroup(tg, page, pages, function)
    if textgroup.textboxes!=[] and textgroup.textboxes!=None:
        for tb in textgroup.textboxes:
            apply_to_textbox(tb, page, pages, function)

def apply_to_textbox(textbox, page, pages, function):
    function(textbox, page, pages)


##############################################################
# Classes to get the probable Textbox type with Heuristics
##############################################################
"""
The existing types are defined in the class TextLineType.
It works like an enum, where each type has an int-number.

Each Textbox has a an instance of ProbableTextboxTypes.
There the Heuristics store how likely the textbox is to be a certain type.
Each type has a score between 0 and 100, while 100 is almost sure.
The most probably type is found by the most_probable() function.
"""

class TextLineType:
    UNKNOWN = 0
    HEADING1_NUMBERED = 1
    #score points: regex->50, fontsize->30,line_count=1->15, word_count=->5,
    HEADING2_NUMBERED = 2
    #score points: regex->50, fontsize->30,line_count=1->15, word_count=->5,
    HEADING3_NUMBERED = 3
    #score points: regex->50, fontsize->30,line_count=1->15, word_count=->5,,
    HEADING_N_NUMBERED = 4
    #score points: regex->40, fontsize->30,line_count=1->15, word_count=->5,
    HEADING1_UNNUMBERED = 5
    #score points: fontsize->40, fontsize_like_numbered->40, line_count=1->15, word_count->5
    HEADING2_UNNUMBERED = 6
    #score points: fontsize->40, fontsize_like_numbered->40, line_count=1->15, word_count->5
    HEADING3_UNNUMBERED = 7
    #score points: fontsize->40, fontsize_like_numbered->40, line_count=1->15, word_count->5
    HEADING_N_UNNUMBERED = 8
    #score points: fontsize->40, fontsize_like_numbered->40, line_count=1->15, word_count->5 ,
    PARAGRAPH = 9
    #score points: font_size and type->50, line_count=1->20, width->20, word_count->10 ,
    FIGURE_LABEL = 10
    #score points: regex->50, italic_font->20, width->15 line_count->15
    """TODO: Process Pictures """
    TABLE_LABEL = 11
    #score points: regex->50, italic_font->20, width->15 line_count->15
    """TODO: Process Tables """
    LISTING_LABEL = 12
    #score points: regex->50, italic_font->20, width->15 line_count->15
    """TODO: Process Listings """
    LIST_ORDERED = 13
    #score points: regex->50, italic_font->20, width->15 line_count->15
    LIST_UNORDERED = 14
    #score points: regex->50, italic_font->20, width->15 line_count->15

    PAGE_NR = 15
    #score points: regex->50, width->30, position->20, line_count->10, word_count->10

NR_OF_TEXTLINE_TYPES = 16

class ProbableTextLineTypes:
    def __init__(self):
        self.score = [0] * NR_OF_TEXTLINE_TYPES
        self.score[TextLineType.UNKNOWN] = 10

    def most_probable(self):
        most_probable_type = 0
        max_score = 0
        for i in range(0, NR_OF_TEXTLINE_TYPES):
            if self.score[i] > max_score:
                most_probable_type = i
                max_score = self.score[i]
                #print('most_probable '+str(most_probable_type)+' score: '+str(max_score))
        return most_probable_type

#####################################
#Converter Functions
#####################################
def str2bbox(bbstr):
    """Converts a bounding box string to the 4 corresponding float values
    Example:
        String: 23.000,42.000,25.000,50.000
        BBox: (x1, y1, x2, y2) = (23.0, 42.0, 25.0, 50.0)
    """
    return tuple(map(float, bbstr.split(",")))

def domdocument2pages(dom):
    """input: the dom as xml-string
    output is a list of Page() objects
    """
    #dom_pages = dom.getElementsByTagName('page')
    return Pages(list(map(dompage2page, dom.getElementsByTagName('page'))))

def dompage2page(dom_page):
    """input: a dom-page as xml-string
    output: a Page() object"""
    id = dom_page.getAttribute('id')
    bbox_parameters = str2bbox(dom_page.getAttribute('bbox'))
    textgroups = list(map(domtextgroup2textgroup, getChildElementsByTagName(dom_page, "textgroup")))
    textboxes = list(map(domtextbox2textbox, getChildElementsByTagName(dom_page, "textbox")))   # all 'textbox' dom-elements in the dom_page are converted into a list of textbox objects
    return Page(ID=id, bbox_parameters=bbox_parameters, textboxes=textboxes, textgroups=textgroups)

def domtextgroup2textgroup(dom_textgroup):
    id = dom_textgroup.getAttribute('id')
    bbox_parameters = str2bbox(dom_textgroup.getAttribute('bbox'))
    textgroups = list(map(domtextgroup2textgroup, getChildElementsByTagName(dom_textgroup, "textgroup")))
    textboxes = list(map(domtextbox2textbox, getChildElementsByTagName(dom_textgroup, "textbox")))
    return Textgroup(id=id, bbox_parameters=bbox_parameters, textboxes=textboxes, textgroups=textgroups)

def domtextbox2textbox(dom_textbox):
    """input: a dom-textbox as xml-string
    output: a Textpage() object
    """
    id = dom_textbox.getAttribute('id')
    bbox_parameters = str2bbox(dom_textbox.getAttribute('bbox'))
    textlines = list(map(domtextline2textline, getChildElementsByTagName(dom_textbox, "textline")))
    return TextBox(id, bbox_parameters, textlines)

def domtextline2textline(dom_textline):
    """input: a dom-textline as xml-string
    output: a Textline() object
    """
    bbox_parameters = str2bbox(dom_textline.getAttribute('bbox'))
    letters = list(map(domtext2letter, getChildElementsByTagName(dom_textline, "text")))
    word_list = make_word_list(letters)
    text = make_text(letters)
    return TextLine(bbox_parameters=bbox_parameters, text=text, wordlist=word_list)

def domtext2letter(dom_text):
    """converts a dom element <text></text> into an object of Class Letter() with all the information
    about font, fontsize and color"""
    try:
        char = dom_text.firstChild.nodeValue
        font = dom_text.getAttribute('font')
        size = dom_text.getAttribute('size')
        color = dom_text.getAttribute('colourspace')
    except AttributeError:
        char = ''
        font = ''
        size = ''
        color = ''
    return Letter(char, font, size, color)

def make_text(letter_list):
    text = ''
    for letter in letter_list:
        text = text + letter.char
    return text

def make_word_list(letter_list):
    """makes a list of Word() from a list of all letters of a textline by checking the word list for
    the space character (' ') and using the make_word() function.
    the words have information about font, size and color """
    letter_buffer=[]
    all_words = []
    for letter in letter_list:
        # append letters to letter_buffer as long no space character occurs
        # if a spate character occurs make a word out of the letters in the word_buffer
        if (letter.char!=' '):
            letter_buffer.append(letter)
        elif len(letter_buffer) > 1:
            all_words.append(make_word(letter_buffer))
            letter_buffer.clear()
    # in the end again make a word out of the remaining letters in the word_buffer under the condition that it doesn't start with a space character
    if len(letter_buffer) > 1:
        if letter_buffer[0].char != ' ':
            all_words.append(make_word(letter_buffer))
    return all_words


def make_word(letter_list):
    """makes a Word() containing the string of the actual word and information about
    font, size and color
    input is a list of letters
    """
    word=Word()
    for letter in letter_list:
        word.string = word.string + letter.char
    word.font = primary(dict_to_sorted_list(font_count(letter_list)))
    word.size = primary(dict_to_sorted_list(size_count(letter_list)))
    return word



##################
#Analyze Functions
###################

def font_count(elements, fonts=[]):
    """see size_count()
    works the same way"""
    fonts = dict()
    for el in elements:
        if el.font not in fonts:
            fonts[el.font] = 1
        else:
            fonts[el.font] += 1
    return fonts

def size_count(elements, sizes=[]):
    """ elements is a list of 'elements' e.g Letter objects or Word objects
    each element has to contain an information about size (wordsize)
    this funcion first makes dictionary with the sizes as a key and the amount of occurance as value
    then it converts the dictionay into a list and sorts it, so that the most used size is the first element
    it returns the list
    """
    sizes = dict()
    for el in elements:
        if el.size not in sizes:
            sizes[el.size] = 1      # ads the size to the dictionary, with the size as the key and the value=1
        else:
            sizes[el.size] += 1     # increases the value of the tuple, where the key is the current size
    return sizes

def primary(list_of_tuples):
    """in a list of tuples, this function returns the second value of the first tupel"""
    #if list_of_tuples!=[] and list_of_tuples!=None:
    if len(list_of_tuples)>=1:
        first_tupel = list_of_tuples[0]
        return first_tupel[1]
    else:
        return None

def dict_to_sorted_list(dictionay):
    lst = list()
    for key, val in dictionay.items():
        lst.append( (val, key) )
    lst.sort(reverse=True)
    return lst

def merge_dicts(dict1, dict2):
    #check if key of first dict also exists in second dict
    #if so: add the values of the key in both dicts. store it in dict2
    for key1 in dict1:
        if key1 in dict2:
            dict2[key1] = dict1[key1] + dict2[key1]
    #update first dict with second. As 'second wins' the updated sum for the common keys is chosen.
    dict1.update(dict2)
    return dict1
