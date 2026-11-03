from functools import cached_property

# docxray stuff
from docxray2.oxml.proxy.document import Document
from docxray2.oxml.xml.main_document import E_Document

from .xml import XmlPart


class MainDocumentPart(XmlPart):
    ELEMENT = E_Document

    @cached_property
    def document(self) -> Document:
        return Document(self.element, self)
