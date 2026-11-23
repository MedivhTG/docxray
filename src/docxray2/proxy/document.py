from typing import TYPE_CHECKING

# docxray stuff
from docxray2.opc.proxy.core_props import CoreProperties
from docxray2.oxml.wml import E_Document
from docxray2.types import PkgFile

from .base import DocxElementProxy
from .custom_props import CustomProperties
from .extf_props import ExtentedProperties

if TYPE_CHECKING:

    # docxray stuff
    from docxray2.parts.main_document import MainDocumentPart  # noqa: F401


class Document(DocxElementProxy[E_Document, "MainDocumentPart"]):
    @property
    def core_props(self) -> CoreProperties | None:
        return self.part.core_props

    @property
    def extf_props(self) -> ExtentedProperties | None:
        return self.part.extf_props

    @property
    def custom_props(self) -> CustomProperties | None:
        return self.part.custom_props

    def get_or_add_core_props(self) -> CoreProperties:
        core_props = self.core_props
        if core_props:
            return core_props
        return self.part._docx_package.create_core_properties_part().core_props

    def get_or_add_extf_props(self) -> ExtentedProperties:
        extf_props = self.extf_props
        if extf_props:
            return extf_props
        return (
            self.part._docx_package.create_extended_file_properties_part().extf_props
        )

    def get_or_add_custom_props(self) -> CustomProperties:
        custom_props = self.custom_props
        if custom_props:
            return custom_props
        return (
            self.part._docx_package.create_custom_file_properties_part().custom_props
        )

    def save(self, file: PkgFile) -> None:
        self.part.save(file)
