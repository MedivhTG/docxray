# -- register custom Part classes with opc package reader --

# docxray stuff
from docxray.opc.constants import CONTENT_TYPE as CT
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.opc.part import Part, PartFactory
from docxray.oxml.trans.parts.document import DocumentPart
from docxray.oxml.trans.parts.image import ImagePart
from docxray.oxml.trans.parts.numbering import NumberingPart
from docxray.oxml.trans.parts.settings import SettingsPart
from docxray.oxml.trans.parts.styles import StylesPart
from docxray.oxml.trans.parts.theme import ThemePart


class TransitionalPartFactory(PartFactory):
    pass


def part_class_selector(content_type: str, reltype: str) -> type[Part] | None:
    """Return part cls for given reltype or content_type.

    Args:
        content_type (str): Given content_type.
        reltype (str): Given reltype.

    Returns:
        type[Part] | None: Part cls or `None` if there is no suitable cls.
    """
    if reltype == RT.IMAGE:
        return ImagePart
    return None


TransitionalPartFactory.part_class_selector = part_class_selector
TransitionalPartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
TransitionalPartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
TransitionalPartFactory.part_type_for[CT.WML_STYLES] = StylesPart
TransitionalPartFactory.part_type_for[CT.WML_SETTINGS] = SettingsPart
TransitionalPartFactory.part_type_for[CT.OFC_THEME] = ThemePart

del (
    CT,
    DocumentPart,
    NumberingPart,
    PartFactory,
    StylesPart,
    SettingsPart,
    part_class_selector,
)
