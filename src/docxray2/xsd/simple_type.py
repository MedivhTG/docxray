from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeVar

from typing_extensions import Sentinel

from .exceptions import XsdValidationError

T = TypeVar("T")
NOT_VALIDATED = Sentinel("NOT_VALIDATED")


@dataclass
class Restriction:
    base: type[SimpleType]


class Union:
    def __init__(self, *member_types: type[SimpleType]) -> None:
        self.member_types = member_types


class SimpleType[T]:
    SCHEMA: Restriction | Union
    FACETS: dict[str, Any] | None = None

    @classmethod
    def validate_schema(
        cls, xml_value: str, facets: dict[str, Any] | None = None
    ) -> T:
        facets_final = cls.FACETS or {}
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
            except XsdValidationError as e:
                exceptions_raised.append(str(e))
        if union_value is NOT_VALIDATED:
            raise XsdValidationError(
                f"None of the types passed the check: [{"; ".join(exceptions_raised)}]"
            )
        return union_value

    @classmethod
    def _validate(cls, xml_value: str, facets: dict[str, Any]) -> Any:
        return xml_value
