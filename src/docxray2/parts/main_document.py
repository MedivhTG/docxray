from functools import cached_property

# docxray stuff
from docxray2.oxml.proxy.document import Document
from docxray2.oxml.xml.main_document import E_Document

from .base import DocxXmlPart


class MainDocumentPart(DocxXmlPart):
    ELEMENT = E_Document

    @cached_property
    def document(self) -> Document:
        return Document(self.element, self)
