"""Initialize `docx` package.

Export the `Document` constructor function and establish the mapping of part-type to
the part-classe that implements that type.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

# docxray stuff
from docxray.api import Document

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import Part

__version__ = "0.1.0"


__all__ = ["Document"]


# -- register custom Part classes with opc package reader --

# docxray stuff
from docxray.opc.constants import CONTENT_TYPE as CT
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.opc.part import PartFactory
from docxray.parts.document import DocumentPart
from docxray.parts.image import ImagePart
from docxray.parts.numbering import NumberingPart
from docxray.parts.styles import StylesPart


def part_class_selector(content_type: str, reltype: str) -> Type[Part] | None:
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
PartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
PartFactory.part_type_for[CT.WML_STYLES] = StylesPart

del (
    CT,
    DocumentPart,
    NumberingPart,
    PartFactory,
    StylesPart,
    part_class_selector,
)
