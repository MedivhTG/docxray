# docxray stuff
from docxray.xsd.primitives import XsdString
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType


class ST_RelationshipId(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
