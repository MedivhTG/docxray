from __future__ import annotations

from datetime import datetime
from enum import Enum, IntFlag, StrEnum
from functools import lru_cache
from typing import Any, Self

# docxray stuff
from docxray2.xsd.w3cdtf import W3CDTFDateTime


class WD_DOCUMENT_SECURITY(IntFlag):
    NONE = 0
    PASSWORD_PROTECTED = 1
    READ_ONLY_RECOMMENDED = 2
    READ_ONLY_ENFORCED = 4
    ANNOTATION_LOCKED = 8

    @classmethod
    def new(cls, value: int) -> Self:
        if (value & ~_WD_DS_MASK) == 0:
            return cls(value)
        return cls(0)


_WD_DS_MASK = (
    WD_DOCUMENT_SECURITY.PASSWORD_PROTECTED
    | WD_DOCUMENT_SECURITY.READ_ONLY_RECOMMENDED
    | WD_DOCUMENT_SECURITY.READ_ONLY_ENFORCED
    | WD_DOCUMENT_SECURITY.ANNOTATION_LOCKED
)


def is_member(value: Any, enum: type[Enum]) -> bool:
    return _is_member_cached(value, enum)


@lru_cache
def _is_member_cached(value: Any, enum: type[Enum]) -> bool:
    return value in {m.value for m in enum}


class WD_CUSTOM_PROPERTY_TYPE(StrEnum):
    TEXT = "string"
    DATE = "datetime"
    NUMBER = "int32"
    BOOLEAN = "boolean"
    NULL = "none"

    @classmethod
    def new(
        cls, value: int | str | W3CDTFDateTime | datetime | bool | None
    ) -> WD_CUSTOM_PROPERTY_TYPE:
        if isinstance(value, bool):
            return cls.BOOLEAN
        if isinstance(value, int):
            return cls.NUMBER
        if isinstance(value, str):
            return cls.TEXT
        if isinstance(value, (W3CDTFDateTime, datetime)):
            return cls.DATE
        if value is None:
            return cls.NULL
        raise TypeError(f"None of type is valid for {value}")
