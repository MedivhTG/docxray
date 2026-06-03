# docxray stuff
from docxray.xsd.facets import MaxInclusiveFacet, MinInclusiveFacet
from docxray.xsd.primitives import XsdLong
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType


class ST_PositiveCoordinate(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdLong)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(0),
        "max_inclusive": MaxInclusiveFacet(27273042316900),
    }
