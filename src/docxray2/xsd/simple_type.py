"""Simple XSD-schema validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeVar

from typing_extensions import Sentinel

from .exceptions import XsdValidationError

T = TypeVar("T")
NOT_VALIDATED = Sentinel("NOT_VALIDATED")


@dataclass(slots=True)
class Restriction:
    """XSD restriction of a simple type.

    Represents ``<xs:restriction base="...">``: validation delegates to
    ``base``, merging this type's facets into the facet set passed down.

    Attributes:
        base (type[SimpleType]): The restricted type. If it is ``SimpleType``
            itself, the deriving type's ``_validate`` is used instead.
    """

    base: type[SimpleType]


class Union:
    """XSD union of simple types.

    Represents ``<xs:union memberTypes="...">``: a value is valid if at least
    one member accepts it. Members are tried in order; the first success wins.
    If all fail, a single ``XsdValidationError`` aggregates their messages.

    Attributes:
        member_types (tuple[type[SimpleType], ...]): Union members, in
            declaration order. Must be non-empty.

    Raises:
        ValueError: If no member types are provided.
    """

    __slots__ = ("member_types",)

    def __init__(self, *member_types: type[SimpleType]) -> None:
        """Initialize the union.

        Args:
            *member_types (type[SimpleType]): Union members. At least one is
                required.

        Raises:
            ValueError: If no member types are provided.
        """
        if not member_types:
            raise ValueError("Must pass at least 1 member type!")
        self.member_types = member_types


class SimpleType[T]:
    """Base class for XSD simple types.

    Subclasses set ``SCHEMA`` (a ``Restriction`` or ``Union``), optionally
    override ``FACETS``, and implement ``_validate`` for the actual coercion.
    ``validate_schema`` is the public entry point; it resolves facets and walks
    the schema accordingly.

    Attributes:
        SCHEMA (Restriction | Union): Schema declaration. Absent means the
            type is validated directly via ``_validate``.
        FACETS (dict[str, Any] | None): Default facets, merged with per-call
            facets (per-call values win).
    """

    SCHEMA: Restriction | Union
    FACETS: dict[str, Any] | None = None

    @classmethod
    def validate_schema(
        cls, xml_value: str, facets: dict[str, Any] | None = None
    ) -> T:
        """Validate and convert a raw XML value according to this type.

        Merges ``cls.FACETS`` with ``facets`` (per-call wins), then:
        no ``SCHEMA`` → ``_validate``; ``Restriction`` → delegate to
        ``SCHEMA.base`` (or ``_validate`` if the base is ``SimpleType``);
        ``Union`` → try members in order, first success wins, otherwise raise
        an aggregated ``XsdValidationError``.

        Args:
            xml_value (str): Raw XML attribute value.
            facets (dict[str, Any] | None): Per-call facet overrides. Defaults
                to ``None``.

        Returns:
            T: Converted value.

        Raises:
            XsdValidationError: If validation fails (directly, via the base
                type, or because no union member accepted the value).
        """
        facets_final = cls.FACETS.copy() if cls.FACETS else {}
        if facets:
            facets_final.update(facets)
        if not hasattr(cls, "SCHEMA"):
            return cls._validate(xml_value, facets_final)
        if isinstance(cls.SCHEMA, Restriction):
            schema = cls.SCHEMA
            if schema.base is SimpleType:
                return cls._validate(xml_value, facets_final)
            return cls.SCHEMA.base.validate_schema(xml_value, facets_final)
        union_value = NOT_VALIDATED
        exceptions_raised = []
        for simple_type in cls.SCHEMA.member_types:
            try:
                union_value = simple_type.validate_schema(
                    xml_value, facets_final
                )
                break
            except XsdValidationError as e:
                exceptions_raised.append(str(e))
        if union_value is NOT_VALIDATED:
            raise XsdValidationError(
                f"None of the types passed the check: [{"; ".join(exceptions_raised)}]"
            )
        return union_value

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> Any:
        """Convert and validate a single raw XML value.

        Extension point for concrete types. The default implementation
        returns the string unchanged.

        Args:
            xml_value (str): Raw XML attribute value.
            facets (dict[str, Any]): Fully resolved facet set (never ``None``).

        Returns:
            Any: Converted value (subclasses should return ``T``).

        Raises:
            XsdValidationError: If the value violates the type's constraints.
        """
        return xml_value
