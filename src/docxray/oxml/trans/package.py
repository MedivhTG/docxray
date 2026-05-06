"""WordprocessingML Package class and related objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.opc.package import OpcPackage

if TYPE_CHECKING:
    from .parts.document import DocumentPart


class TransitionalPackage(OpcPackage):
    @property
    def main_document_part(self) -> DocumentPart:
        """Return a reference to the main document part for this package.

        Examples include a document part for a WordprocessingML package, a presentation
        part for a PresentationML package, or a workbook part for a SpreadsheetML
        package.
        """
        from .parts.document import DocumentPart

        return self.part_related_by(RT.OFFICE_DOCUMENT, DocumentPart)
