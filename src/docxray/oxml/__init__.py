# -- register custom Part classes with opc package reader --

# docxray stuff
from docxray.opc.constants import CONTENT_TYPE as CT
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.opc.part import Part, PartFactory
from docxray.oxml.transitional.parts.document import DocumentPart
from docxray.oxml.transitional.parts.image import ImagePart
from docxray.oxml.transitional.parts.numbering import NumberingPart
from docxray.oxml.transitional.parts.styles import StylesPart


def part_class_selector(content_type: str, reltype: str) -> type[Part] | None:
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
