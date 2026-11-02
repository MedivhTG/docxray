from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

from .pkg_uri import PkgURI
from .rel import Relationship, Relationships

if TYPE_CHECKING:
    from .package import OpcPackage


class Part:
    def __init__(
        self,
        part_name: PkgURI,
        content_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> None:
        self._part_name = part_name
        self._content_type = content_type
        self._blob = blob
        self._package = package

    def load_rel(
        self,
        rel_type: str,
        target: Part | str,
        rel_id: str,
        is_external: bool = False,
    ) -> Relationship:
        return self.rels.add_relationship(
            rel_type, target, rel_id, is_external
        )

    @cached_property
    def rels(self) -> Relationships:
        return Relationships(self._part_name.baseURI)

    @classmethod
    def load(
        cls,
        part_name: PkgURI,
        content_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Self:
        return cls(part_name, content_type, blob, package)

    def after_unmarshal(self) -> None:
        pass


class PartFactory:
    part_type_for: dict[str, type[Part]] = {}
    DEFAULT_PART_TYPE = Part

    @classmethod
    def create_part(
        cls,
        part_name: PkgURI,
        content_type: str,
        rel_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Part:
        PartClass = cls._part_cls_for(content_type)
        return PartClass.load(part_name, content_type, blob, package)

    @classmethod
    def _part_cls_for(cls, content_type: str) -> type[Part]:
        return cls.part_type_for.get(content_type, cls.DEFAULT_PART_TYPE)
