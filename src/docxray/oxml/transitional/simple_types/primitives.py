# mypy: disable-error-code="override"

import re
from datetime import datetime
from enum import StrEnum
from typing import Any, TypedDict, Unpack

from .exceptions import XsdTypeError
from .facets import EnumerationFacet, LengthFacet, PatternFacet
from .xsd import XsdPrimitive


class StringFacets(TypedDict, total=False):
    enum: EnumerationFacet
    length: LengthFacet
    pattern: PatternFacet


class XsdString(XsdPrimitive):
    @classmethod
    def validate(
        cls, xml_obj: Any, **facets: Unpack[StringFacets]
    ) -> str | StrEnum:
        if not isinstance(xml_obj, str):
            raise XsdTypeError.construct(xml_obj, cls)
        enum = facets.pop("enum", EnumerationFacet())
        if enum._members:
            members = enum._members
            if xml_obj not in members:
                raise XsdTypeError.construct(
                    xml_obj, cls, f"expected members `{members}`"
                )
        length = facets.pop("length", LengthFacet())
        if length.value and len(xml_obj) != length.value:
            raise XsdTypeError.construct(
                xml_obj, cls, f"length expected {length.value}"
            )
        pattern = facets.pop("pattern", PatternFacet())
        if pattern.value and not re.match(pattern.value, xml_obj):
            raise XsdTypeError.construct(
                xml_obj, cls, f"pattern mismatch {pattern.value}"
            )
        enum_cls = enum.enum_cls
        if enum_cls:
            return enum_cls(xml_obj)
        return xml_obj


class XsdDateTime(XsdPrimitive):
    @classmethod
    def validate(cls, xml_obj: str, **facets: Any) -> datetime:
        try:
            return datetime.fromisoformat(xml_obj.replace("Z", "+00:00"))
        except Exception:
            raise XsdTypeError.construct(xml_obj, cls, "ISO format")


class XsdInteger(XsdPrimitive):
    INT_RE: str = r"^-?(0|[1-9][0-9]*)$"

    @classmethod
    def validate(cls, xml_obj: str, **facets: Any) -> int:
        if not re.match(cls.INT_RE, xml_obj):
            raise XsdTypeError.construct(xml_obj, cls, f"pattern {cls.INT_RE}")
        return int(xml_obj)


class HexBinaryFacets(TypedDict, total=False):
    length: LengthFacet


class XsdHexBinary(XsdPrimitive):
    HEX_RE: str = r"^[0-9A-Fa-f]*$"

    @classmethod
    def validate(
        cls, xml_obj: str, **facets: Unpack[HexBinaryFacets]
    ) -> bytes:
        length = facets.pop("length", LengthFacet())
        if not re.match(cls.HEX_RE, xml_obj):
            raise XsdTypeError.construct(xml_obj, cls, f"pattern {cls.HEX_RE}")
        binary = bytes.fromhex(xml_obj)
        if length.value and len(binary) != length.value:
            raise XsdTypeError.construct(
                binary, cls, f"expected length {length.value}"
            )
        return binary


class XsdBoolean(XsdPrimitive):
    FALSE = {"false", "0"}
    TRUE = {"true", "1"}

    @classmethod
    def validate(cls, xml_obj: str, **facets: Any) -> bool:
        if xml_obj in cls.FALSE:
            return False
        if xml_obj in cls.TRUE:
            return True
        raise XsdTypeError.construct(
            xml_obj, cls, f"expected true `{cls.TRUE}` or false `{cls.FALSE}`"
        )
