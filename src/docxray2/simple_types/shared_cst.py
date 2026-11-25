import re

# docxray stuff
from docxray2.xsd.primitives import (
    XsdBoolean,
    XsdHexBinary,
    XsdNCName,
    XsdString,
    XsdToken,
    XsdUnsignedLong,
)
from docxray2.xsd.simple_type import Restriction, SimpleType, Union


class ST_Lang(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_HexColorRGB(SimpleType[bytes]):
    SCHEMA = Restriction(XsdHexBinary)
    FACETS = {"length": 3}


class ST_Panose(SimpleType[bytes]):
    SCHEMA = Restriction(XsdHexBinary)
    FACETS = {"length": 10}


class ST_CalendarType(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_AlgClass(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_CryptProv(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_AlgType(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_ColorType(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


ST_GUID_RE = re.compile(
    r"\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}"
)


class ST_Guid(SimpleType[str]):
    SCHEMA = Restriction(XsdToken[str])
    FACETS = {"pattern": ST_GUID_RE}


class ST_OnOff1(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_OnOff(SimpleType):
    SCHEMA = Union(XsdBoolean, ST_OnOff1)


class ST_String(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_XmlName(SimpleType[str]):
    SCHEMA = Restriction(XsdNCName)
    FACETS = {"minLength": 1, "maxLength": 255}


class ST_TrueFalse(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_TrueFalseBlank(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_UnsignedDecimalNumber(SimpleType[int]):
    SCHEMA = Restriction(XsdUnsignedLong)


ST_UNIVERSAL_MEASURE_RE = re.compile(r"-?[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)")


class ST_UniversalMeasure(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": ST_UNIVERSAL_MEASURE_RE}


ST_POSITIVE_UNIVERSAL_MEASURE_RE = re.compile(
    r"[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)"
)


class ST_PositiveUniversalMeasure(ST_UniversalMeasure):
    SCHEMA = Restriction(ST_UniversalMeasure)
    FACETS = {"pattern": ST_POSITIVE_UNIVERSAL_MEASURE_RE}


class ST_TwipsMeasure(SimpleType):
    SCHEMA = Union(ST_UnsignedDecimalNumber, ST_PositiveUniversalMeasure)


class ST_VerticalAlignRun(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_Xstring(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_XAlign(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_YAlign(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


class ST_ConformanceClass(SimpleType[str]):
    SCHEMA = Restriction(XsdString)


ST_PERCENTAGE_RE = re.compile(r"-?[0-9]+(\.[0-9]+)?%")


class ST_Percentage(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": ST_PERCENTAGE_RE}


ST_FIXED_PERCENTAGE_RE = re.compile(
    r"-?((100)|([0-9][0-9]?))(\.[0-9][0-9]?)?%"
)


class ST_FixedPercentage(ST_Percentage):
    SCHEMA = Restriction(ST_Percentage)
    FACETS = {"pattern": ST_FIXED_PERCENTAGE_RE}


ST_POSITIVE_PERCENTAGE_RE = re.compile(r"[0-9]+(\.[0-9]+)?%")


class ST_PositivePercentage(ST_Percentage):
    SCHEMA = Restriction(ST_Percentage)
    FACETS = {"pattern": ST_POSITIVE_PERCENTAGE_RE}


ST_POSITIVE_FIXED_PERCENTAGE_RE = re.compile(
    r"((100)|([0-9][0-9]?))(\.[0-9][0-9]?)?%"
)


class ST_PositiveFixedPercentage(ST_Percentage):
    SCHEMA = Restriction(ST_Percentage)
    FACETS = {"pattern": ST_POSITIVE_FIXED_PERCENTAGE_RE}
