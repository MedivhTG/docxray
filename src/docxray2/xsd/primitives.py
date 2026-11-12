import binascii
import math
import re
import struct
from base64 import b64decode, b64encode
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, TypeVar

from .exceptions import XsdStringifyError, XsdValidationError
from .simple_type import Restriction, SimpleType
from .w3cdtf import W3CDTFDateTime

ANY_T = TypeVar("ANY_T")


class XsdAnySimpleType(SimpleType[ANY_T]):
    pass


STRING_T = TypeVar("STRING_T", bound=str | StrEnum)


class XsdString(XsdAnySimpleType[STRING_T]):
    SCHEMA = Restriction(SimpleType)
    FACETS = {"whitespace": "preserve"}

    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> str | StrEnum:
        xml_value = cls.apply_whitespace(xml_value, **facets)
        cls.validate_length(xml_value, **facets)
        cls.validate_pattern(xml_value, **facets)
        enum_member = cls.validate_enumeration(xml_value, **facets)
        if enum_member is not None:
            return enum_member
        return xml_value


class XsdNormalizedString(XsdString[STRING_T]):
    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> str | StrEnum:
        xml_value = cls.apply_whitespace(xml_value, "replace")
        return super()._validate(xml_value, facets)

    @classmethod
    def _stringify(cls, py_value: str, facets: dict[str, Any]) -> str:
        return cls.apply_whitespace(py_value, "replace")


class XsdToken(XsdNormalizedString[STRING_T]):
    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> str | StrEnum:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        return super()._validate(xml_value, facets)

    @classmethod
    def _stringify(cls, py_value: str, facets: dict[str, Any]) -> str:
        py_value = cls.apply_whitespace(py_value, "collapse")
        return super()._stringify(py_value, facets)


URI_INVALID_RE = re.compile(r"%(?![0-9A-Fa-f]{2})|#.*#")


class XsdAnyUri(XsdAnySimpleType[str]):
    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> str:
        if URI_INVALID_RE.search(xml_value) is not None:
            raise XsdValidationError(f"Invalid anyURI value: `{xml_value}`")
        return xml_value


NAME_RE = re.compile(r"^[^\W\d:][\w.:-]*$", re.UNICODE)
NCNAME_RE = re.compile(r"^[^\W\d][\w.-]*$", re.UNICODE)


class XsdName(XsdString[str]):
    FACETS = {"pattern": NAME_RE}


class XsdNCName(XsdName):
    FACETS = {"pattern": NCNAME_RE}


class XsdID(XsdNCName):
    pass


W3CDTF_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class XsdDateTime(XsdAnySimpleType[W3CDTFDateTime]):
    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> W3CDTFDateTime:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        try:
            w3cdtf = W3CDTFDateTime.from_datetime(xml_value)
        except ValueError as e:
            raise XsdValidationError(f"W3CDTF validation error: {e}")
        cls.validate_datetime_ranges(w3cdtf, **facets)
        return w3cdtf

    @classmethod
    def _stringify(
        cls, py_value: W3CDTFDateTime | datetime, facets: dict[str, str]
    ) -> str:
        if isinstance(py_value, W3CDTFDateTime):
            return py_value.str_datetime()
        try:
            return W3CDTFDateTime.from_datetime_python(py_value).str_datetime()
        except ValueError as e:
            raise XsdStringifyError(e)


class XsdGYear(XsdAnySimpleType[W3CDTFDateTime]):
    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> W3CDTFDateTime:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        try:
            w3cdtf = W3CDTFDateTime.from_gyear(xml_value)
        except ValueError as e:
            raise XsdValidationError(f"W3CDTF validation error: {e}")
        cls.validate_datetime_ranges(w3cdtf, **facets)
        return w3cdtf

    @classmethod
    def _stringify(
        cls, py_value: W3CDTFDateTime | datetime, facets: dict[str, Any]
    ) -> str:
        if isinstance(py_value, W3CDTFDateTime):
            return py_value.str_gyear()
        try:
            return W3CDTFDateTime.from_datetime_python(py_value).str_gyear()
        except ValueError as e:
            raise XsdStringifyError(e)


class XsdGYearMonth(XsdAnySimpleType[W3CDTFDateTime]):
    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> W3CDTFDateTime:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        try:
            w3cdtf = W3CDTFDateTime.from_gyearmonth(xml_value)
        except ValueError as e:
            raise XsdValidationError(f"W3CDTF validation error: {e}")
        cls.validate_datetime_ranges(w3cdtf, **facets)
        return w3cdtf

    @classmethod
    def _stringify(
        cls, py_value: W3CDTFDateTime | datetime, facets: dict[str, Any]
    ) -> str:
        if isinstance(py_value, W3CDTFDateTime):
            return py_value.str_gyearmonth()
        try:
            return W3CDTFDateTime.from_datetime_python(
                py_value
            ).str_gyearmonth()
        except ValueError as e:
            raise XsdStringifyError(e)


class XsdDate(XsdAnySimpleType[W3CDTFDateTime]):
    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> W3CDTFDateTime:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        try:
            w3cdtf = W3CDTFDateTime.from_date(xml_value)
        except ValueError as e:
            raise XsdValidationError(f"W3CDTF validation error: {e}")
        cls.validate_datetime_ranges(w3cdtf, **facets)
        return w3cdtf

    @classmethod
    def _stringify(
        cls, py_value: W3CDTFDateTime | datetime, facets: dict[str, Any]
    ) -> str:
        if isinstance(py_value, W3CDTFDateTime):
            return py_value.str_date()
        try:
            return W3CDTFDateTime.from_datetime_python(py_value).str_date()
        except ValueError as e:
            raise XsdStringifyError(e)


DECIMAL_LEXICAL_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")

NUM_T = TypeVar("NUM_T", bound=int | Decimal)


class XsdDecimal(XsdAnySimpleType[NUM_T]):
    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> Decimal:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        d = cls.to_decimal(xml_value)
        cls.validate_numeric_ranges(d, **facets)
        cls.validate_fraction_digits(d, **facets)
        cls.validate_total_digits(d, **facets)
        return d

    @classmethod
    def to_decimal(cls, xml_value: str) -> Decimal:
        if not DECIMAL_LEXICAL_RE.match(xml_value):
            raise XsdValidationError(
                f"Invalid xs:decimal lexical form: {xml_value!r}"
            )
        return Decimal(xml_value)


class XsdInteger(XsdDecimal[int]):
    @classmethod
    def _validate(  # type: ignore[override]
        cls, xml_value: str, facets: dict[str, Any]
    ) -> int:
        facets["fraction_digits"] = 0
        d = super()._validate(xml_value, facets)
        return int(d)


class XsdLong(XsdInteger):
    FACETS = {
        "min_inclusive": -9223372036854775808,
        "max_inclusive": 9223372036854775807,
    }


class XsdInt(XsdLong):
    FACETS = {"min_inclusive": -2147483648, "max_inclusive": 2147483647}


class XsdShort(XsdInt):
    FACETS = {"min_inclusive": -32768, "max_inclusive": 32767}


class XsdByte(XsdShort):
    FACETS = {"min_inclusive": -128, "max_inclusive": 127}


class XsdNonNegativeInteger(XsdInteger):
    FACETS = {"min_inclusive": 0}


class XsdUnsignedLong(XsdNonNegativeInteger):
    FACETS = {"max_inclusive": 18446744073709551615}


class XsdUnsignedInt(XsdUnsignedLong):
    FACETS = {"max_inclusive": 4294967295}


class XsdUnsignedShort(XsdUnsignedInt):
    FACETS = {"max_inclusive": 65535}


class XsdUnsignedByte(XsdUnsignedShort):
    FACETS = {"max_inclusive": 255}


FLOAT_SPECIAL = {"INF": math.inf, "-INF": -math.inf, "NaN": math.nan}
FLOAT_RE = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


class XsdFloat(XsdAnySimpleType[float]):
    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> float:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        f = cls.to_float(xml_value)
        cls.validate_numeric_ranges(f, **facets)
        return f

    @classmethod
    def _stringify(cls, py_value: float, facets: dict[str, Any]) -> str:
        if math.isnan(py_value):
            return "NaN"
        if math.isinf(py_value):
            return "INF" if py_value > 0 else "-INF"
        try:
            v32 = struct.unpack(">f", struct.pack(">f", py_value))[0]
        except OverflowError:
            return "INF" if py_value > 0 else "-INF"
        s = repr(v32)
        if s == "-0.0":
            return "-0"
        if s == "0.0":
            return "0"
        if "e" in s:
            mantissa, exp = s.split("e")
            s = f"{mantissa}E{exp}"
        return s

    @classmethod
    def to_float(cls, xml_value: str) -> float:
        if xml_value in FLOAT_SPECIAL:
            return FLOAT_SPECIAL[xml_value]
        if not FLOAT_RE.match(xml_value):
            raise XsdValidationError(
                f"Invalid xs:float lexical value: {xml_value!r}"
            )
        return float(xml_value)


DOUBLE_RE = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


class XsdDouble(XsdAnySimpleType[float]):
    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> float:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        d = cls.to_double(xml_value)
        cls.validate_numeric_ranges(d, **facets)
        return d

    @classmethod
    def _stringify(cls, py_value: Any, facets: dict[str, Any]) -> str:
        if math.isnan(py_value):
            return "NaN"
        if math.isinf(py_value):
            return "INF" if py_value > 0 else "-INF"
        s = repr(py_value)
        if s == "-0.0":
            return "-0"
        if s == "0.0":
            return "0"
        if "e" in s:
            mantissa, exp = s.split("e")
            s = f"{mantissa}E{exp}"
        return s

    @classmethod
    def to_double(cls, xml_value: str) -> float:
        if xml_value in FLOAT_SPECIAL:
            return FLOAT_SPECIAL[xml_value]
        if not DOUBLE_RE.match(xml_value):
            raise XsdValidationError(
                f"Invalid xs:double lexical value: {xml_value!r}"
            )
        return float(xml_value)


BOOLEAN_FALSE_XML_VALUES = {"false", "0"}
BOOLEAN_TRUE_XML_VALUES = {"true", "1"}


class XsdBoolean(XsdAnySimpleType[bool]):
    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> bool:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        return cls.to_bool(
            xml_value, BOOLEAN_FALSE_XML_VALUES, BOOLEAN_TRUE_XML_VALUES
        )

    @classmethod
    def to_bool(
        cls, xml_value: str, false_set: set[str], true_set: set[str]
    ) -> bool:
        if xml_value in false_set:
            return False
        if xml_value in true_set:
            return True
        raise XsdValidationError(
            f"Invalid xs:boolean lexical form: not in `{list(*false_set, *true_set)}`"
        )


class XsdBase64Binary(XsdAnySimpleType[bytes]):
    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> bytes:
        xml_value = cls.apply_whitespace(xml_value, "collapse")
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumeration(xml_value, **facets)
        cls.validate_length(xml_value, **facets)
        try:
            return b64decode(xml_value, validate=True)
        except (binascii.Error, ValueError) as e:
            raise XsdValidationError(f"Invalid xs:base64Binary: {e}")

    @classmethod
    def _stringify(cls, py_value: bytes, facets: dict[str, Any]) -> str:
        try:
            return b64encode(py_value).decode("ascii")
        except (binascii.Error, TypeError, ValueError) as e:
            raise XsdStringifyError(f"Invalid xs:base64Binary: {e}")
