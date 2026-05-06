# docxray stuff
from docxray.xsd.facets import (
    EnumerationFacet,
    LengthFacet,
    PatternFacet,
)
from docxray.xsd.primitives import (
    XsdDateTime,
    XsdHexBinary,
    XsdInteger,
    XsdString,
)
from docxray.xsd.xsd import (
    XsdRestriction,
    XsdSimpleType,
)

from .enums import (
    SE_Border,
    SE_HexColorAuto,
    SE_Merge,
    SE_MultilevelType,
    SE_StyleType,
    SE_TblStyleOverrideType,
    SE_TblWidth,
    SE_Underline,
)


class ST_DateTime(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdDateTime)


class ST_DecimalNumber(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInteger)


class ST_LongHexNumber(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdHexBinary)
    FACETS = {"length": LengthFacet(value=4)}


class ST_Cnf(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {
        "length": LengthFacet(value=12),
        "pattern": PatternFacet(value=r"[01]*"),
    }


class ST_StyleType(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_StyleType)}


class ST_TblStyleOverrideType(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_TblStyleOverrideType)}


class ST_Merge(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_Merge)}


class ST_Underline(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_Underline)}


class ST_MultiLevelType(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_MultilevelType)}


class ST_TblWidth(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_TblWidth)}


class ST_Border(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_Border)}


class ST_HexColorAuto(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_HexColorAuto)}
