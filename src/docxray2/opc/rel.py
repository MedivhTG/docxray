from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .part import Part


class Relationships(dict[str, "Relationship"]):
    def __init__(self, baseURI: str) -> None:
        self._baseURI = baseURI
        self._target_parts_referenced: dict[str, str | Part] = {}

    def add_relationship(
        self,
        rel_type: str,
        target: Part | str,
        rel_id: str,
        is_external: bool = False,
    ) -> Relationship:
        rel = Relationship(
            rel_id, rel_type, target, self._baseURI, is_external
        )
        self[rel_id] = rel
        if not is_external:
            self._target_parts_referenced[rel_id] = target
        return rel


@dataclass
class Relationship:
    rel_id: str
    rel_type: str
    target: str | Part
    baseURI: str
    external: bool = False
