# docxray stuff
from docxray2.oxml.elements.main_document import E_Document
from docxray2.oxml.proxy.base import ElementProxy


class Document(ElementProxy[E_Document]):
    pass
