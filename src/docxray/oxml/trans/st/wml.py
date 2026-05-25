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
    XsdUnion,
)

from .enums import (
    SE_HINT,
    SE_JC,
    SE_LEVEL_SUFFIX,
    SE_NUMBER_FORMAT,
    SE_TEXT_ALIGNMENT,
    SE_TEXT_DIRECTION,
    SE_THEME,
    SE_Border,
    SE_HexColorAuto,
    SE_Merge,
    SE_MultilevelType,
    SE_StyleType,
    SE_TblStyleOverrideType,
    SE_TblWidth,
    SE_Underline,
)
from .shared_common import ST_Percentage, ST_UniversalMeasure


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


class ST_UnqualifiedPercentage(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInteger)


class ST_DecimalNumberOrPercent(XsdSimpleType):
    SCHEMA = XsdUnion(ST_UnqualifiedPercentage, ST_Percentage)


class ST_MeasurementOrPercent(XsdSimpleType):
    SCHEMA = XsdUnion(ST_DecimalNumberOrPercent, ST_UniversalMeasure)


class ST_ShortHexNumber(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdHexBinary)
    FACETS = {"length": LengthFacet(value=2)}


class ST_SignedTwipsMeasure(XsdSimpleType):
    SCHEMA = XsdUnion(XsdInteger, ST_UniversalMeasure)


class ST_Jc(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_JC)}


class ST_TextAlignment(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_TEXT_ALIGNMENT)}


class ST_NumberFormat(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_NUMBER_FORMAT)}


class ST_LevelSuffix(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_LEVEL_SUFFIX)}


class ST_TextDirection(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_TEXT_DIRECTION)}


class ST_Hint(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_HINT)}


class ST_Theme(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_THEME)}
