import re
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
        "some_shit": 3,
    }


class XsdInt(XsdLong):
    FACETS = {"min_inclusive": -2147483648, "max_inclusive": 2147483647}
