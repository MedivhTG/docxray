# docxray stuff
from docxray.xsd.facets import EnumerationFacet
from docxray.xsd.primitives import XsdString
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType

from .enums import SE_JC_OMATH


class ST_Jc(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_JC_OMATH)}
