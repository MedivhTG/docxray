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
    SE_BR_CLEAR,
    SE_BR_TYPE,
    SE_HEIGHT_RULE,
    SE_HEX_COLOR_AUTO,
    SE_HINT,
    SE_JC,
    SE_JC_TABLE,
    SE_LEVEL_SUFFIX,
    SE_LINE_SPACING_RULE,
    SE_NUMBER_FORMAT,
    SE_TEXT_ALIGNMENT,
    SE_TEXT_DIRECTION,
    SE_THEME,
    SE_THEME_COLOR,
    SE_UNDERLINE,
    SE_VERTICAL_JC,
    SE_BORDER,
    SE_Merge,
    SE_MultilevelType,
    SE_StyleType,
    SE_TblStyleOverrideType,
    SE_TblWidth,
)
from .shared_common import (
    ST_HexColorRGB,
    ST_Percentage,
    ST_PositiveUniversalMeasure,
    ST_UniversalMeasure,
    ST_UnsignedDecimalNumber,
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
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_UNDERLINE)}


class ST_MultiLevelType(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_MultilevelType)}


class ST_TblWidth(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_TblWidth)}


class ST_Border(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_BORDER)}


class ST_HexColorAuto(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_HEX_COLOR_AUTO)}


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


class ST_BrType(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_BR_TYPE)}


class ST_BrClear(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_BR_CLEAR)}


class ST_HeightRule(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_HEIGHT_RULE)}


class ST_LineSpacingRule(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_LINE_SPACING_RULE)}


class ST_VerticalJc(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_VERTICAL_JC)}


class ST_HexColor(XsdSimpleType):
    SCHEMA = XsdUnion(ST_HexColorAuto, ST_HexColorRGB)


class ST_ThemeColor(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_THEME_COLOR)}


class ST_UcharHexNumber(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdHexBinary)
    FACETS = {"length": LengthFacet(1)}


class ST_EighthPointMeasure(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_UnsignedDecimalNumber)


class ST_PointMeasure(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_UnsignedDecimalNumber)


class ST_HpsMeasure(XsdSimpleType):
    SCHEMA = XsdUnion(ST_UnsignedDecimalNumber, ST_PositiveUniversalMeasure)


class ST_JcTable(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)
    FACETS = {"enum": EnumerationFacet(enum_cls=SE_JC_TABLE)}
