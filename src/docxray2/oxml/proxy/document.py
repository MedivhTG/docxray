from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.proxy.core_props import CoreProperties
from docxray2.oxml.xml.main_document import E_Document

from .base import DocxElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.parts.main_document import MainDocumentPart  # noqa: F401


class Document(DocxElementProxy[E_Document, "MainDocumentPart"]):
    @property
    def core_props(self) -> CoreProperties:
        return self.part.core_props
