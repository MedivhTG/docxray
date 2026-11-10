import re
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, TypeVar

from .exceptions import XsdValidationError
from .simple_type import Restriction, SimpleType


class XsdAnySimpleType(SimpleType[str]):
    SCHEMA = Restriction(SimpleType)


STRING_T = TypeVar("STRING_T", bound=str | StrEnum)


class XsdString(SimpleType[STRING_T]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> str | StrEnum:
        whitespace = facets.get("whitespace", "preserve")
        xml_value = cls.apply_whitespace(xml_value, whitespace)
        cls.validate_length(xml_value, **facets)
        cls.validate_pattern(xml_value, **facets)
        validated = cls.validate_enumaration(xml_value, **facets)
        if validated is not None:
            return validated
        return xml_value


URI_INVALID_PATTERN = re.compile(r"%(?![0-9A-Fa-f]{2})|#.*#")


class XsdAnyUri(SimpleType[str]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> str:
        if URI_INVALID_PATTERN.search(xml_value) is not None:
            raise XsdValidationError(f"Invalid anyURI value: `{xml_value}`")
        return xml_value


NAME_PATTERN = re.compile(r"^[^\W\d:][\w.:-]*$", re.UNICODE)
NCNAME_PATTERN = re.compile(r"^[^\W\d][\w.-]*$", re.UNICODE)


class XsdName(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": NAME_PATTERN}


class XsdNCName(SimpleType[str]):
    SCHEMA = Restriction(XsdName)
    FACETS = {"pattern": NCNAME_PATTERN}


class XsdID(SimpleType[str]):
    SCHEMA = Restriction(XsdNCName)


W3CDTF_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class XsdDateTime(SimpleType[datetime]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> datetime:
        xml_value = cls.apply_whitespace(xml_value)
        cls.validate_pattern(xml_value, **facets)
        cls.validate_enumaration(xml_value, **facets)
        dt = cls.convert_to_datetime_from_iso8601(xml_value)
        cls.validate_datetime(dt, **facets)
        return dt

    @classmethod
    def _stringify(cls, py_value: datetime) -> str:
        utc_dt = py_value.astimezone(UTC)
        return utc_dt.strftime(W3CDTF_FORMAT)
