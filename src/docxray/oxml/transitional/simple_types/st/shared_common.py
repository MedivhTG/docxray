# docxray stuff
from docxray.oxml.transitional.simple_types.facets import EnumerationFacet
from docxray.oxml.transitional.simple_types.primitives import (
    XsdBoolean,
    XsdString,
)
from docxray.oxml.transitional.simple_types.xsd import (
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
