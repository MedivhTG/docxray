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

    @property
    def content_type(self) -> str:
        return self._content_type

    @cached_property
    def rels(self) -> Relationships:
        return Relationships(self._part_name.baseURI)

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

    def after_unmarshal(self) -> None:
        pass

    @classmethod
    def load(
        cls,
        part_name: PkgURI,
        content_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Self:
        return cls(part_name, content_type, blob, package)


class XmlPart(Part):
    @classmethod
    def load(
        cls,
        part_name: PkgURI,
        content_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Self:
        return super().load(part_name, content_type, blob, package)
