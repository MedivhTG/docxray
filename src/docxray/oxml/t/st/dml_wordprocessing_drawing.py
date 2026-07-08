# docxray stuff
from docxray.xsd.primitives import XsdUnsignedInt
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType


class ST_WrapDistance(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdUnsignedInt)
