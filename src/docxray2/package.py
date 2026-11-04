from functools import cached_property

# docxray stuff
from docxray2.parts.core_properties import CorePropertiesPart
from docxray2.parts.main_document import MainDocumentPart

from .ns import RELATIONSHIP_TYPE
from .opc.package import OpcPackage


class DocxPackage(OpcPackage):
    @cached_property
    def main_document_part(self) -> MainDocumentPart:
        return self.part_related_by(
            RELATIONSHIP_TYPE.MAIN_DOCUMENT, MainDocumentPart
        )

    @cached_property
    def core_properties_part(self) -> CorePropertiesPart:
        return self.part_related_by(
            RELATIONSHIP_TYPE.CORE_PROPERTIES, CorePropertiesPart
        )
