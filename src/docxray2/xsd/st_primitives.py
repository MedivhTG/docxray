import re
from enum import StrEnum
from typing import Any

from .exceptions import XsdValidationError
from .simple_type import Restriction, SimpleType


class XsdAnySimpleType(SimpleType[str]):
    SCHEMA = Restriction(SimpleType)


class XsdString(SimpleType[str | StrEnum]):
    SCHEMA = Restriction(SimpleType)

    @classmethod
    def _validate(
        cls, xml_value: str, facets: dict[str, Any]
    ) -> str | StrEnum:
        length = facets.get("length")
        min_length = facets.get("min_length")
        max_length = facets.get("max_length")
        if length is not None and (
            max_length is not None or min_length is not None
        ):
            raise ValueError(
                "Length and (MinLength or MaxLength) are mutually exclusive"
            )
        if length is not None and len(xml_value) != length:
            raise XsdValidationError(
                f"Length must be `{length}`, got `{len(xml_value)}`"
            )
        if min_length is not None and len(xml_value) < min_length:
            raise XsdValidationError(
                f"MinLength must be `{min_length}`, got `{len(xml_value)}`"
            )
        if max_length is not None and len(xml_value) > max_length:
            raise XsdValidationError(
                f"MaxLength must be `{max_length}`, got `{len(xml_value)}`"
            )
        enumeration: type[StrEnum] | None = facets.get("enumeration")
        if enumeration is not None:
            if xml_value in enumeration._value2member_map_:
                return enumeration(xml_value)
            raise XsdValidationError(
                f"Got `{xml_value}`, must be in values: {enumeration.__members__}"
            )
        pattern = facets.get("pattern")
        if pattern is not None and re.search(pattern, xml_value) is None:
            raise XsdValidationError(
                f"Pattern mismatch for `{xml_value}` <= `{pattern}`"
            )
        return xml_value


class XsdAnyUri(SimpleType[str]):
    SCHEMA = Restriction(SimpleType)
    URI_INVALID_PATTERN = re.compile(r"%(?![0-9A-Fa-f]{2})|#.*#")

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> str:
        if cls.URI_INVALID_PATTERN.search(xml_value) is not None:
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
