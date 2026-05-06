# docxray stuff
from docxray.xsd.facets import EnumerationFacet, PatternFacet
from docxray.xsd.primitives import (
    XsdBoolean,
    XsdString,
)
from docxray.xsd.xsd import (
    XsdRestriction,
    XsdSimpleType,
    XsdUnion,
)

from .enums import SE_OnOff1, SE_VerticalAlignRun


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
