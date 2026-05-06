# -- register custom Part classes with opc package reader --

# docxray stuff
from docxray.opc.constants import CONTENT_TYPE as CT
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.opc.part import Part, PartFactory
from docxray.oxml.trans.parts.document import DocumentPart
from docxray.oxml.trans.parts.image import ImagePart
from docxray.oxml.trans.parts.numbering import NumberingPart
from docxray.oxml.trans.parts.styles import StylesPart


class TransitionalPartFactory(PartFactory):
    pass


def part_class_selector(content_type: str, reltype: str) -> type[Part] | None:
    if reltype == RT.IMAGE:
        return ImagePart
    return None


TransitionalPartFactory.part_class_selector = part_class_selector
TransitionalPartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
TransitionalPartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
TransitionalPartFactory.part_type_for[CT.WML_STYLES] = StylesPart

del (
    CT,
    DocumentPart,
    NumberingPart,
    PartFactory,
    StylesPart,
    part_class_selector,
)
