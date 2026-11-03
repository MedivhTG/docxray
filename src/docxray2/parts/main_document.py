from functools import cached_property

# docxray stuff
from docxray2.opc.part import XmlPart
from docxray2.proxy.document import Document


class MainDocumentPart(XmlPart):
    @cached_property
    def document(self) -> Document:
        return Document()
