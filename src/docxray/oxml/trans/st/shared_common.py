# docxray stuff
from docxray.xsd.facets import EnumerationFacet, LengthFacet, PatternFacet
from docxray.xsd.primitives import (
    XsdBoolean,
    XsdHexBinary,
    XsdString,
    XsdUnsignedLong,
)
from docxray.xsd.xsd import (
    XsdRestriction,
    XsdSimpleType,
    XsdUnion,
)

from .enums import SE_Y_ALIGN, SE_OnOff1, SE_VerticalAlignRun


class ST_String(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)


class ST_OnOff1(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(SE_OnOff1)}


class ST_OnOff(XsdSimpleType):
    SCHEMA = XsdUnion(XsdBoolean, ST_OnOff1)


class ST_VerticalAlignRun(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(SE_VerticalAlignRun)}


class ST_UniversalMeasure(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {
        "pattern": PatternFacet(r"-?[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)")
    }


class ST_Percentage(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"pattern": PatternFacet(r"-?[0-9]+(\.[0-9]+)?%")}


class ST_UnsignedDecimalNumber(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdUnsignedLong)


class ST_PositiveUniversalMeasure(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_UniversalMeasure)
    FACETS = {"pattern": PatternFacet(r"[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)")}


class ST_TwipsMeasure(XsdSimpleType):
    SCHEMA = XsdUnion(ST_UnsignedDecimalNumber, ST_PositiveUniversalMeasure)


class ST_Lang(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)


class ST_HexColorRGB(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdHexBinary)
    FACETS = {"length": LengthFacet(3, True)}


class ST_YAlign(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(SE_Y_ALIGN)}
