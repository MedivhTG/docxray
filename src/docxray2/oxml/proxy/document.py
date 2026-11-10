from typing import TYPE_CHECKING

# docxray stuff
from docxray2.opc.proxy.core_props import CoreProperties
from docxray2.oxml.xml.main_document import E_Document
from docxray2.types import PkgFile

from .base import DocxElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.parts.main_document import MainDocumentPart  # noqa: F401


class Document(DocxElementProxy[E_Document, "MainDocumentPart"]):
    @property
    def core_props(self) -> CoreProperties | None:
        return self.part.core_props

    def save(self, file: PkgFile) -> None:
        self.part.save(file)
