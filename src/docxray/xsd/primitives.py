# mypy: disable-error-code="override"

import re
from datetime import datetime
from enum import StrEnum
from typing import Any, TypedDict, Unpack

from dateutil import parser

from .facets import (
    EnumerationFacet,
    LengthFacet,
    PatternFacet,
)
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
            cls.xsd_err(xml_obj)
        enum = facets.pop("enum", EnumerationFacet())
        if enum._members:
            members = enum._members
            if xml_obj not in members:
                cls.xsd_err(xml_obj, f"expected members `{members}`")
        length = facets.pop("length", LengthFacet())
        if length.value and len(xml_obj) != length.value:
            cls.xsd_err(xml_obj, f"length expected {length.value}")
        pattern = facets.pop("pattern", PatternFacet())
        if pattern.value and not re.match(pattern.value, xml_obj):
            cls.xsd_err(xml_obj, f"pattern mismatch {pattern.value}")
        enum_cls = enum.enum_cls
        if enum_cls:
            return enum_cls(xml_obj)
        return xml_obj


class XsdDateTime(XsdPrimitive):
    @classmethod
    def validate(cls, xml_obj: str, **facets: Any) -> datetime:
        try:
            return parser.isoparse(xml_obj)
        except Exception as e:
            cls.xsd_err(
                xml_obj,
                f"internal error while converting str to datetime [{e}]",
            )


class XsdInteger(XsdPrimitive):
    INT_RE: str = r"^[+-]?\d+$"

    @classmethod
    def validate(cls, xml_obj: str, **facets: Any) -> int:
        if not re.match(cls.INT_RE, xml_obj):
            cls.xsd_err(xml_obj, f"pattern mismatch {cls.INT_RE}")
        return int(xml_obj)


class HexBinaryFacets(TypedDict, total=False):
    length: LengthFacet


class XsdHexBinary(XsdPrimitive):
    HEX_RE: str = r"^[0-9a-fA-F]*$"

    @classmethod
    def validate(
        cls, xml_obj: str, **facets: Unpack[HexBinaryFacets]
    ) -> bytes:
        length = facets.pop("length", LengthFacet())
        if not re.match(cls.HEX_RE, xml_obj):
            cls.xsd_err(xml_obj, f"pattern mismatch {cls.HEX_RE}")
        binary = bytes.fromhex(xml_obj)
        if length.value and len(binary) != length.value:
            cls.xsd_err(binary, f"expected length {length.value}")
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
        cls.xsd_err(
            xml_obj, f"expected true `{cls.TRUE}` or false `{cls.FALSE}`"
        )


class XsdUnsignedLong(XsdPrimitive):
    MIN_UINT64 = 0
    MAX_UINT64 = 18446744073709551615

    @classmethod
    def validate(cls, xml_obj: str, **facets: Any) -> int:
        try:
            num = int(xml_obj)
            if cls.MIN_UINT64 > num > cls.MAX_UINT64:
                cls.xsd_err(
                    num,
                    f"Number must be between {cls.MIN_UINT64} and {cls.MAX_UINT64}",
                )
            return num
        except ValueError as e:
            cls.xsd_err(
                xml_obj, f"internal error while converting str to int [{e}]"
            )
