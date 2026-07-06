# docxray stuff
from docxray.xsd.facets import (
    EnumerationFacet,
    MaxInclusiveFacet,
    MinInclusiveFacet,
)
from docxray.xsd.primitives import (
    XsdByte,
    XsdInt,
    XsdLong,
    XsdString,
    XsdToken,
    XsdUnsignedInt,
)
from docxray.xsd.xsd import XsdRestriction, XsdSimpleType, XsdUnion

from .enums import (
    SE_PITCH_FAMILY,
    SE_PRESET_COLOR_VAL,
    SE_SCHEME_COLOR_VAL,
    SE_SYSTEM_COLOR_VAL,
)
from .shared_common import ST_FixedPercentage as ST_FixedPercentage_COMMON
from .shared_common import ST_Percentage as ST_Percentage_COMMON
from .shared_common import (
    ST_PositiveFixedPercentage as ST_PositiveFixedPercentage_COMMON,
)
from .shared_common import (
    ST_PositivePercentage as ST_PositivePercentage_COMMON,
)


class ST_PositiveCoordinate(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdLong)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(0),
        "max_inclusive": MaxInclusiveFacet(27273042316900),
    }


class ST_DrawingElementId(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdUnsignedInt)


class ST_PercentageDecimal(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInt)


class ST_Percentage(XsdSimpleType):
    SCHEMA = XsdUnion(ST_PercentageDecimal, ST_Percentage_COMMON)


class ST_Angle(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdInt)


class ST_PositiveFixedAngle(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_Angle)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(0),
        "max_inclusive": MaxInclusiveFacet(21600000),
    }


class ST_SystemColorVal(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdToken)
    FACETS = {"enum": EnumerationFacet(SE_SYSTEM_COLOR_VAL)}


class ST_SchemeColorVal(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdToken)
    FACETS = {"enum": EnumerationFacet(SE_SCHEME_COLOR_VAL)}


class ST_PresetColorVal(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdToken)
    FACETS = {"enum": EnumerationFacet(SE_PRESET_COLOR_VAL)}


class ST_PositiveFixedPercentageDecimal(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_PercentageDecimal)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(0),
        "max_inclusive": MaxInclusiveFacet(100000),
    }


class ST_PositiveFixedPercentage(XsdSimpleType):
    SCHEMA = XsdUnion(
        ST_PositiveFixedPercentageDecimal, ST_PositiveFixedPercentage_COMMON
    )


class ST_FixedPercentageDecimal(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_PercentageDecimal)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(-100000),
        "max_inclusive": MaxInclusiveFacet(100000),
    }


class ST_FixedPercentage(XsdSimpleType):
    SCHEMA = XsdUnion(ST_FixedPercentageDecimal, ST_FixedPercentage_COMMON)


class ST_PositivePercentageDecimal(XsdSimpleType):
    SCHEMA = XsdRestriction(ST_PercentageDecimal)
    FACETS = {
        "min_inclusive": MinInclusiveFacet(0),
    }


class ST_PositivePercentage(XsdSimpleType):
    SCHEMA = XsdUnion(
        ST_PositivePercentageDecimal, ST_PositivePercentage_COMMON
    )


class ST_TextTypeface(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdString)


class ST_PitchFamily(XsdSimpleType):
    SCHEMA = XsdRestriction(XsdByte)
    FACETS = {"enum": EnumerationFacet(SE_PITCH_FAMILY)}
