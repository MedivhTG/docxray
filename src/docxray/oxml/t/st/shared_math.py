# docxray stuff
from docxray.xsd.facets import (
    EnumerationFacet,
    MaxInclusiveFacet,
    MaxLengthFacet,
    MinInclusiveFacet,
)
from docxray.xsd.primitives import XsdInteger, XsdString, XsdUnsignedInt
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType

from .enums import (
    SE_F_TYPE,
    SE_JC_OMATH,
    SE_LIM_LOC,
    SE_SCRIPT,
    SE_SHP,
    SE_STYLE,
    SE_TOP_BOT,
)


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


class ST_SpacingRule(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInteger)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(0),
        "max_inclusive": MaxInclusiveFacet(4),
    }


class ST_UnSignedInteger(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdUnsignedInt)


class ST_FType(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_F_TYPE)}


class ST_LimLoc(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_LIM_LOC)}


class ST_Script(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_SCRIPT)}


class ST_Style(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_STYLE)}
