from __future__ import annotations

from abc import abstractmethod
from typing import Any

# docxray stuff
from docxray.oxml.transitional.simple_types.exceptions import XsdBaseError


class XsdFacet:
    pass


class XsdPrimitive:
    @classmethod
    @abstractmethod
    def validate(cls, xml_obj: Any, **facets: Any) -> Any: ...


class XsdRestriction:
    def __init__(self, base: type[XsdSimpleType | XsdPrimitive]) -> None:
        self._base = base

    @property
    def base(self) -> type[XsdSimpleType | XsdPrimitive]:
        return self._base


class XsdUnion:
    def __init__(
        self, *member_types: type[XsdPrimitive | XsdSimpleType]
    ) -> None:
        self._member_types = member_types

    @property
    def member_types(self) -> tuple[type[XsdPrimitive | XsdSimpleType], ...]:
        return self._member_types


class XsdSimpleType:
    SCHEMA: Any = XsdUnion()
    FACETS: dict[str, XsdFacet] = {}

    def __init__(self, xml_obj: Any) -> None:
        self._xml_obj = xml_obj

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def xml_obj(self) -> Any:
        return self.xml_obj

    def validate(self) -> Any:
        if isinstance(self.SCHEMA, XsdRestriction):
            return self._validate_restriction(self.xml_obj)
        return self._validate_union(self.xml_obj)

    def _validate_restriction(self, restriction: XsdRestriction) -> Any:
        return self._validate_from_schema(restriction.base)

    def _validate_union(self, union: XsdUnion) -> Any:
        err_raised: XsdBaseError | None = None
        for member in union.member_types:
            try:
                return self._validate_from_schema(member)
            except XsdBaseError as e:
                err_raised = e
        if err_raised is not None:
            raise err_raised

    def _validate_from_schema(
        self, xsd_schema: type[XsdPrimitive | XsdSimpleType]
    ) -> Any:
        if issubclass(xsd_schema, XsdPrimitive):
            return xsd_schema.validate(self.xml_obj, **self.FACETS)
        return xsd_schema(self.xml_obj).validate()
