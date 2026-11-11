"""Simple XSD-schema validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from re import Pattern
from typing import Any, Literal, TypeVar

from typing_extensions import Sentinel

from .exceptions import XsdStringifyError, XsdValidationError

T = TypeVar("T")
NOT_VALIDATED = Sentinel("NOT_VALIDATED")
NOT_STRINGIFIED = Sentinel("NOT_STRINGIFIED")


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
    __facets_mro__: dict[str, Any]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        facets_mro = {}
        for base in reversed(cls.__mro__):
            facets = base.__dict__.get("FACETS")
            if isinstance(facets, dict):
                facets_mro.update(facets)
        cls.__facets_mro__ = facets_mro

    @classmethod
    def facets(cls) -> dict[str, Any]:
        return cls.__facets_mro__.copy()

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
        facets_final = cls.facets()
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
            except (ValueError, XsdValidationError) as e:
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

    @classmethod
    def stringify(
        cls, py_value: Any, facets: dict[str, Any] | None = None
    ) -> str:
        facets_final = cls.facets()
        if facets:
            facets_final.update(facets)
        if not hasattr(cls, "SCHEMA"):
            return cls._stringify(py_value, facets_final)
        if isinstance(cls.SCHEMA, Restriction):
            schema = cls.SCHEMA
            if schema.base is SimpleType:
                return cls._stringify(py_value, facets_final)
            return cls.SCHEMA.base.stringify(py_value, facets_final)
        # We will get first type (as rule)
        str_value = NOT_STRINGIFIED
        exceptions_raised = []
        for simple_type in cls.SCHEMA.member_types:
            try:
                str_value = simple_type.stringify(py_value, facets_final)  # type: ignore[assignment]
                break
            except (ValueError, XsdStringifyError) as e:
                exceptions_raised.append(str(e))
        if str_value is NOT_STRINGIFIED:
            raise XsdStringifyError(
                f"None of the types can stingify value: [{"; ".join(exceptions_raised)}]"
            )
        return str_value

    @classmethod
    def _stringify(cls, py_value: Any, facets: dict[str, Any]) -> str:
        return cls.apply_whitespace(str(py_value), **facets)

    @classmethod
    def apply_whitespace(
        cls,
        xml_value: str,
        whitespace: Literal["preserve", "replace", "collapse"] = "preserve",
        **kwargs: dict[str, Any],
    ) -> str:
        if whitespace == "preserve":
            return xml_value
        elif whitespace == "collapse":
            replaced = (
                xml_value.replace("\t", " ")
                .replace("\n", " ")
                .replace("\r", " ")
            )
            return re.sub(r" +", " ", replaced).strip()
        elif whitespace == "replace":
            return (
                xml_value.replace("\t", " ")
                .replace("\n", " ")
                .replace("\r", " ")
            )
        else:
            raise ValueError(f"Unkown whitespace mode: {whitespace}")

    @classmethod
    def validate_datetime_ranges(
        cls,
        dt: datetime,
        min_inclusive: datetime | None = None,
        max_inclusive: datetime | None = None,
        min_exclusive: datetime | None = None,
        max_exclusive: datetime | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        cls._check_min_max_facets(
            min_inclusive, max_inclusive, min_exclusive, max_exclusive
        )
        dt_utc = cls._dt_to_utc(dt)
        lo_inc = (
            cls._dt_to_utc(min_inclusive)
            if min_inclusive is not None
            else None
        )
        hi_inc = (
            cls._dt_to_utc(max_inclusive)
            if max_inclusive is not None
            else None
        )
        lo_exc = (
            cls._dt_to_utc(min_exclusive)
            if min_exclusive is not None
            else None
        )
        hi_exc = (
            cls._dt_to_utc(max_exclusive)
            if max_exclusive is not None
            else None
        )

        if lo_inc is not None and dt_utc < lo_inc:
            raise XsdValidationError(
                f"Datetime {dt} less than {min_inclusive}"
            )
        if hi_inc is not None and dt_utc > hi_inc:
            raise XsdValidationError(
                f"Datetime {dt} greater than {max_inclusive}"
            )
        if lo_exc is not None and dt_utc <= lo_exc:
            raise XsdValidationError(
                f"Datetime {dt} less or equal than {min_exclusive}"
            )
        if hi_exc is not None and dt_utc >= hi_exc:
            raise XsdValidationError(
                f"Datetime {dt} greater or equal than {max_exclusive}"
            )

    @classmethod
    def validate_numeric_ranges(
        cls,
        num: int | Decimal,
        min_inclusive: int | Decimal | None = None,
        max_inclusive: int | Decimal | None = None,
        min_exclusive: int | Decimal | None = None,
        max_exclusive: int | Decimal | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        cls._check_min_max_facets(
            min_inclusive, max_inclusive, min_exclusive, max_exclusive
        )
        if min_inclusive is not None and num < min_inclusive:
            raise XsdValidationError(
                f"Numeric {num} less than {min_inclusive}"
            )
        if max_inclusive is not None and num > max_inclusive:
            raise XsdValidationError(
                f"Numeric {num} greater than {max_inclusive}"
            )
        if min_exclusive is not None and num <= min_exclusive:
            raise XsdValidationError(
                f"Numeric {num} less or equal than {min_exclusive}"
            )
        if max_exclusive is not None and num >= max_exclusive:
            raise XsdValidationError(
                f"Numeric {num} greater or equal than {max_exclusive}"
            )

    @classmethod
    def validate_fraction_digits(
        cls,
        num: Decimal | int,
        fraction_digits: int | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        if fraction_digits is None:
            return
        if isinstance(num, int):
            num = Decimal(num)
        normalized = num.normalize()
        exp = normalized.as_tuple().exponent
        if not isinstance(exp, int):
            raise XsdValidationError(
                f"Unexpected exponent for finite decimal: {exp!r}"
            )
        frac = -exp if exp < 0 else 0
        if frac > fraction_digits:
            raise XsdValidationError(
                f"fractionDigits exceeded: {num!r} has {frac} fraction digits, "
                f"max {fraction_digits}"
            )

    @classmethod
    def validate_total_digits(
        cls,
        num: Decimal | int,
        total_digits: int | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        if total_digits is None:
            return
        if isinstance(num, int):
            num = Decimal(num)
        actual = len(num.as_tuple().digits)
        if actual > total_digits:
            raise XsdValidationError(
                f"totalDigits exceeded: {num!r} has {actual} significant digits, "
                f"max {total_digits}"
            )

    @classmethod
    def validate_length(
        cls,
        xml_value: str,
        length: int | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        len_bounds_on = max_length is not None or min_length is not None
        if length is not None and len_bounds_on:
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

    @classmethod
    def validate_enumeration(
        cls,
        xml_value: str,
        enumeration: type[StrEnum] | None = None,
        **kwargs: dict[str, Any],
    ) -> StrEnum | None:
        if enumeration is not None:
            if xml_value in enumeration._value2member_map_:
                return enumeration(xml_value)
            raise XsdValidationError(
                f"Got `{xml_value}`, must be in values: {enumeration.__members__}"
            )
        return None

    @classmethod
    def validate_pattern(
        cls,
        xml_value: str,
        pattern: str | Pattern | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        if pattern is not None and re.search(pattern, xml_value) is None:
            raise XsdValidationError(
                f"Pattern mismatch for `{xml_value}` <= `{pattern}`"
            )

    @classmethod
    def _dt_to_utc(cls, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)

    @classmethod
    def _check_min_max_facets(
        cls,
        min_inclusive: Any | None,
        max_inclusive: Any | None,
        min_exclusive: Any | None,
        max_exclusive: Any | None,
    ) -> None:
        inc_on = min_inclusive is not None or max_inclusive is not None
        exc_on = min_exclusive is not None or max_exclusive is not None
        if inc_on and exc_on:
            raise ValueError(
                "Inclusive and Exclusive params are mutually exclusive"
            )
