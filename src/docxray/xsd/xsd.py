"""Main module for XSD-validation (XSD - XML Schema Definition, W3C)."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, NoReturn

from .exceptions import XsdBaseError, XsdTypeError


class XsdFacet:
    """Class with provided arguments for XSD type."""

    pass


class XsdPrimitive:
    """Primitive XSD-type defined in W3C."""

    @classmethod
    def xsd_err(cls, obj: Any, extra: str = "") -> NoReturn:
        """Cosntruct and raise error.

        Args:
            obj (Any): Fiven object for representation.
            extra (str, optional): Extra info for error. Defaults to "".

        Raises:
            XsdTypeError.construct: Standard XSD error.

        Returns:
            NoReturn: Method always raises.
        """
        raise XsdTypeError.construct(obj, cls, extra)

    @classmethod
    @abstractmethod
    def validate(cls, xml_obj: Any, **facets: Any) -> Any:
        """Validate xml object through special logic described in method with given facets.

        Args:
            xml_obj (Any): Usually string representation of an xml value inside of XML-tree.

        Returns:
            Any: Validated object (can be `str`, `int`, etc.)
        """


class XsdRestriction:
    """Class-container for given XSD simple type or primitive."""

    def __init__(self, base: type[XsdPrimitive | XsdSimpleType]) -> None:
        self._base = base

    @property
    def base(self) -> type[XsdPrimitive | XsdSimpleType]:
        """XSD simple type or primitive cls."""
        return self._base


class XsdUnion:
    """Class-container for given list of XSD simple types or primitives."""

    def __init__(
        self, *member_types: type[XsdPrimitive | XsdSimpleType]
    ) -> None:
        self._member_types = member_types

    @property
    def member_types(self) -> tuple[type[XsdPrimitive | XsdSimpleType], ...]:
        """Contained tuple of an XSD simple types or primitives."""
        return self._member_types


class XsdSimpleType:
    """Main class for creating simple XSD types for XML-validation.

    `SCHEMA` - class variable with class container `XsdRestriction` or `XsdUnion` used for validation.

    `FACETS` - class variable dictionary needed for configuring validation thorough `SCHEMA` members.
    """

    SCHEMA: Any = XsdUnion()
    FACETS: dict[str, XsdFacet] = {}

    def __init__(self, xml_obj: Any) -> None:
        self._xml_obj = xml_obj

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def xml_obj(self) -> Any:
        """Contained XML-object value."""
        return self._xml_obj

    def validate(self) -> Any:
        """Validate contained `xml_obj`.

        Returns:
            Any: Validated and converted xml object.
        """
        if isinstance(self.SCHEMA, XsdRestriction):
            return self._validate_restriction(self.SCHEMA)
        return self._validate_union(self.SCHEMA)

    def _validate_restriction(self, restriction: XsdRestriction) -> Any:
        """Validate `xml_obj` through given xsd restriction container schema.

        Args:
            restriction (XsdRestriction): Given restriction xsd schema.

        Returns:
            Any: Validated and converted xml object.
        """
        return self._validate_from_schema(restriction.base)

    def _validate_union(self, union: XsdUnion) -> Any:
        """Validate `xml_obj` through given xsd union container schema.

        Args:
            union (XsdUnion): Given union xsd schema.

        Returns:
            Any: Validated and converted xml object.
        """
        err_raised: XsdBaseError | None = None
        for member in union.member_types:
            try:
                return self._validate_from_schema(member)
            except XsdBaseError as e:
                err_raised = e
        if err_raised is not None:
            raise err_raised

    def _validate_from_schema(
        self, schema: type[XsdPrimitive | XsdSimpleType]
    ) -> Any:
        """Validate `xml_obj` through given schema.

        Args:
            schema (type[XsdPrimitive  |  XsdSimpleType]): Primitive or simple type vlidation schema.

        Returns:
            Any: Validated and converted xml object.
        """
        if issubclass(schema, XsdPrimitive):
            return schema.validate(self.xml_obj, **self.FACETS)
        return schema(self.xml_obj).validate()
