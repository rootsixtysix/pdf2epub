"""provides funtions to convert the pdf file into an string in xml format"""

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import BytesIO
from xml.dom.minidom import parseString

# regular expressions for invalid characters to remove frome the xmlstring
# ASCII invalid characters
RE_XML_ILLEGAL_ASCII = r"[\x01-\x09\x0B\x0C\x0E-\x1F\x7F]"
# unicode invalid characters
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                     u'|' + \
                     u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                      (chr(0xd800),chr(0xdbff),chr(0xdc00),chr(0xdfff),
                       chr(0xd800),chr(0xdbff),chr(0xdc00),chr(0xdfff),
                       chr(0xd800),chr(0xdbff),chr(0xdc00),chr(0xdfff),
                       )

class Options:
    """options for pdf mining"""
    def __init__(self):
        """constructor"""
        self.pagenos = list()
        self.maxpages = 0
        self.password = ""
        self.caching = True
        self.codec = "utf-8"
        self.layoutmode = "normal"
        self.pageno = 1
        self.scale = 1
        self.showpageno = True
        self.laparams = LAParams()

def pdf2dom(file, options=Options()):
    """opens the given pdf file and makes a xmlstring out of it
    Mainly using the pdfminer library"""
    with open(file, 'rb') as fp:
        returnstring = BytesIO()
        resourcemanager = PDFResourceManager(caching=options.caching)
        device = XMLConverter(resourcemanager,
                                returnstring,
                                codec=options.codec,
                                laparams=options.laparams)
        interpreter = PDFPageInterpreter(resourcemanager, device)
        for page in PDFPage.get_pages(fp,
                                        options.pagenos,
                                        maxpages=options.maxpages,
                                        password=options.password,
                                        caching=options.caching,
                                        check_extractable=True):
            interpreter.process_page(page)
        device.close()
        xml_string = returnstring.getvalue()
        returnstring.close()
        xml_string = fix_empty_brackets(replace_control_chars(xml_string))
        dom = parseString(xml_string)
    return dom

def replace_control_chars(s, replace=u""):
    """ replaces invalid control chars in the xml string (see regular expressions above)
    http://chase-seibert.github.io/blog/2011/05/20/stripping-control-characters-in-python.html
    """
    if s:
        import re
        s = s.decode("utf-8")

        # unicode invalid characters
        s = re.sub(RE_XML_ILLEGAL, replace, s)
        # ascii control characters
        s = re.sub(RE_XML_ILLEGAL_ASCII, replace, s)
        # empty brackets
        s = re.sub('<text></text>', '<text> </text>', s)

        s = s.encode("utf-8")
        return s

def fix_empty_brackets(s):
    if s:
        import re
        s = s.decode("utf-8")
        # empty brackets
        s = re.sub('<text></text>', '<text> </text>', s)
        s = s.encode("utf-8")
        return s
