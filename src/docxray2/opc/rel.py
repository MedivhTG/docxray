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

    def part_with_rel_type(self, rel_type: str) -> Part:
        return self._get_rel_of_type(rel_type).target_part

    def _get_rel_of_type(self, rel_type: str) -> Relationship:
        matching = [rel for rel in self.values() if rel.rel_type == rel_type]
        if len(matching) == 0:
            raise KeyError(f"No matched rel of type {rel_type}")
        if len(matching) > 1:
            raise ValueError(f"Multiple rels of type {rel_type}")
        return matching[0]


@dataclass
class Relationship:
    rel_id: str
    rel_type: str
    target: str | Part
    baseURI: str
    external: bool = False

    @property
    def target_part(self) -> Part:
        if self.external or isinstance(self.target, str):
            raise ValueError("Target part is external resource (link)")
        return self.target
