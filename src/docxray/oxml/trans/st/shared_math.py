# docxray stuff
from docxray.xsd.facets import (
    EnumerationFacet,
    MaxInclusiveFacet,
    MaxLengthFacet,
    MinInclusiveFacet,
)
from docxray.xsd.primitives import XsdInteger, XsdString
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType

from .enums import SE_JC_OMATH, SE_SHP, SE_TOP_BOT


class ST_Jc(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_JC_OMATH)}


class ST_Char(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"max_length": MaxLengthFacet(value=1)}


class ST_TopBot(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_TOP_BOT)}


class ST_Integer2(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInteger)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(-2),
        "max_inclusive": MaxInclusiveFacet(2),
    }


class ST_Integer255(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInteger)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(1),
        "max_inclusive": MaxInclusiveFacet(255),
    }


class ST_Shp(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_SHP)}
