from functools import cached_property

from .ns import RELATIONSHIP_TYPE
from .opc.package import OpcPackage
from .parts import MainDocumentPart


class DocxPackage(OpcPackage):
    @cached_property
    def main_document_part(self) -> MainDocumentPart:
        return self.part_related_by(
            RELATIONSHIP_TYPE.MAIN_DOCUMENT, MainDocumentPart
        )
