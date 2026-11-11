import re
from datetime import datetime
from enum import StrEnum
from typing import Any, TypeVar

from .exceptions import XsdStringifyError, XsdValidationError
from .simple_type import Restriction, SimpleType
from .w3cdtf import W3CDTFDateTime


class XsdAnySimpleType(SimpleType[str]):
    SCHEMA = Restriction(SimpleType)


STRING_T = TypeVar("STRING_T", bound=str | StrEnum)


class XsdString(SimpleType[STRING_T]):
    SCHEMA = Restriction(SimpleType)
    FACETS = {"whitespace": "preserve"}

    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> str | StrEnum:
        whitespace = facets.get("whitespace", "preserve")
        xml_value = cls.apply_whitespace(xml_value, whitespace)
        cls.validate_length(xml_value, **facets)
        cls.validate_pattern(xml_value, **facets)
        validated = cls.validate_enumeration(xml_value, **facets)
        if validated is not None:
            return validated
        return xml_value


URI_INVALID_RE = re.compile(r"%(?![0-9A-Fa-f]{2})|#.*#")


class XsdAnyUri(SimpleType[str]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> str:
        if URI_INVALID_RE.search(xml_value) is not None:
            raise XsdValidationError(f"Invalid anyURI value: `{xml_value}`")
        return xml_value


NAME_RE = re.compile(r"^[^\W\d:][\w.:-]*$", re.UNICODE)
NCNAME_RE = re.compile(r"^[^\W\d][\w.-]*$", re.UNICODE)


class XsdName(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": NAME_RE}


class XsdNCName(SimpleType[str]):
    SCHEMA = Restriction(XsdName)
    FACETS = {"pattern": NCNAME_RE}


class XsdID(SimpleType[str]):
    SCHEMA = Restriction(XsdNCName)


W3CDTF_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class XsdDateTime(SimpleType[W3CDTFDateTime]):
    SCHEMA = Restriction(SimpleType)

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


class XsdGYear(SimpleType[W3CDTFDateTime]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> Any:
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


class XsdGYearMonth(SimpleType[W3CDTFDateTime]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> Any:
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


class XsdDate(SimpleType[W3CDTFDateTime]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> Any:
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
