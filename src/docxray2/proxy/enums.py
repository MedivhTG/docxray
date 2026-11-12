from enum import Enum, IntFlag
from functools import lru_cache
from typing import Any, Self


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
