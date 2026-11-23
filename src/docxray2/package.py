from functools import cached_property
from typing import TypeVar, cast

# docxray stuff
from docxray2.exceptions import DocxMissingPart
from docxray2.opc.oxml.parser import OpcOxml
from docxray2.opc.parts.base import OpcXmlPart
from docxray2.opc.parts.core_properties import CorePropertiesPart
from docxray2.oxml.parser import Oxml
from docxray2.parts.base import DocxXmlPart
from docxray2.parts.custom_file_properties import CustomFilePropertiesPart
from docxray2.parts.extended_file_properties import ExtendedFilePropertiesPart
from docxray2.parts.main_document import MainDocumentPart

from .ns import RELATIONSHIP_TYPE
from .opc.package import Package

PART_T = TypeVar("PART_T", bound=OpcXmlPart | DocxXmlPart)


class DocxPackage(Package):
    @cached_property
    def main_document_part(self) -> MainDocumentPart:
        part = self.part_related_by(
            RELATIONSHIP_TYPE.MAIN_DOCUMENT, MainDocumentPart
        )
        if part is None:
            raise DocxMissingPart(
                f"Part `{RELATIONSHIP_TYPE.MAIN_DOCUMENT}` not found"
            )
        return part

    @property
    def core_properties_part(self) -> CorePropertiesPart | None:
        return self.part_related_by(
            RELATIONSHIP_TYPE.CORE_PROPERTIES, CorePropertiesPart
        )

    @property
    def extended_file_properties_part(
        self,
    ) -> ExtendedFilePropertiesPart | None:
        return self.part_related_by(
            RELATIONSHIP_TYPE.EXTENDED_PROPERTIES, ExtendedFilePropertiesPart
        )

    @property
    def custom_file_properties_part(self) -> CustomFilePropertiesPart | None:
        return self.part_related_by(
            RELATIONSHIP_TYPE.CUSTOM_PROPERTIES, CustomFilePropertiesPart
        )

    def create_core_properties_part(self) -> CorePropertiesPart:
        return self._create_xml_part(CorePropertiesPart)

    def create_extended_file_properties_part(
        self,
    ) -> ExtendedFilePropertiesPart:
        return self._create_xml_part(ExtendedFilePropertiesPart)

    def create_custom_file_properties_part(self) -> CustomFilePropertiesPart:
        return self._create_xml_part(CustomFilePropertiesPart)

    def _create_xml_part(self, part_xml_cls: type[PART_T]) -> PART_T:
        elm_cls = cast(
            "type[OpcOxml | Oxml]",
            part_xml_cls.ELEMENT,  # pyright: ignore[reportGeneralTypeIssues]
        )
        part_xml = part_xml_cls(
            part_name=part_xml_cls.PART_NAME_DEFAULT,
            content_type=part_xml_cls.CONTENT_TYPE_DEFAULT,
            element=elm_cls.new(nsmap_mode="full_nsmap"),
        )
        self.rels.get_or_add(part_xml_cls.RELATIONSHIP_TYPE_DEFAULT, part_xml)
        return part_xml
