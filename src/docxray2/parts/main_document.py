from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray2.opc.parts.core_properties import CorePropertiesPart
from docxray2.opc.proxy.core_props import CoreProperties
from docxray2.oxml.proxy.document import Document
from docxray2.oxml.proxy.extf_props import ExtentedFileProperties
from docxray2.oxml.xml.main_document import E_Document
from docxray2.parts.extended_file_properties import ExtendedFilePropertiesPart
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

    @property
    def core_props_part(self) -> CorePropertiesPart | None:
        return self._docx_package.core_properties_part

    @property
    def extf_props_part(self) -> ExtendedFilePropertiesPart | None:
        return self._docx_package.extended_file_properties_part

    @property
    def core_props(self) -> CoreProperties | None:
        if self.core_props_part is None:
            return None
        return self.core_props_part.core_props

    @property
    def extf_props(self) -> ExtentedFileProperties | None:
        if self.extf_props_part is None:
            return None
        return self.extf_props_part.extf_props

    def save(self, file: PkgFile) -> None:
        self._docx_package.save(file)

    @property
    def _docx_package(self) -> DocxPackage:

        # docxray stuff
        from docxray2.package import DocxPackage

        assert isinstance(self.package, DocxPackage)
        return self.package
