from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.proxy.core_props import CoreProperties
from docxray2.oxml.proxy.document import Document
from docxray2.oxml.xml.main_document import E_Document
from docxray2.types import PkgFile

from .base import DocxXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.package import DocxPackage


class MainDocumentPart(DocxXmlPart[E_Document]):
    ELEMENT = E_Document

    @cached_property
    def document(self) -> Document:
        return Document(self.element, self)

    @cached_property
    def core_props(self) -> CoreProperties:
        return self._docx_package.core_properties_part.core_props

    def save(self, file: PkgFile) -> None:
        self._docx_package.save(file)

    @property
    def _docx_package(self) -> DocxPackage:
        # docxray stuff
        from docxray2.package import DocxPackage

        assert isinstance(self.package, DocxPackage)
        return self.package
