"""Module with standard W3C xsd facets."""

from collections.abc import ValuesView
from enum import StrEnum
from functools import cached_property

from .xsd import XsdFacet


class LengthFacet(XsdFacet):
    def __init__(
        self, value: int | None = None, fixed: bool | None = None
    ) -> None:
        self._value = value
        self._fixed = fixed

    @property
    def value(self) -> int | None:
        return self._value

    @property
    def fixed(self) -> bool | None:
        return self._fixed


class MaxLengthFacet(XsdFacet):
    def __init__(self, value: int | None = None) -> None:
        self._value = value

    @property
    def value(self) -> int | None:
        return self._value


class PatternFacet(XsdFacet):
    def __init__(self, value: str | None = None) -> None:
        self._value = value

    @property
    def value(self) -> str | None:
        return self._value


class EnumerationFacet(XsdFacet):
    def __init__(self, enum_cls: type[StrEnum] | None = None) -> None:
        self._enum_cls = enum_cls

    @property
    def enum_cls(self) -> type[StrEnum] | None:
        return self._enum_cls

    @cached_property
    def _members(self) -> ValuesView[StrEnum] | None:
        if self.enum_cls is None:
            return None
        return self.enum_cls.__members__.values()


class MinInclusiveFacet(XsdFacet):
    def __init__(self, value: int | None = None) -> None:
        self._value = value

    @property
    def value(self) -> int | None:
        return self._value


class MaxInclusiveFacet(MinInclusiveFacet):
    pass
