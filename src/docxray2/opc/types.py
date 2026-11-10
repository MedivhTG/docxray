from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from .pkg_uri import PkgURI

if TYPE_CHECKING:
    from .package import Package
    from .part import Part


class PartFactory(Protocol):
    @classmethod
    def create_part(
        cls,
        part_name: PkgURI,
        content_type: str,
        rel_type: str,
        blob: bytes,
        package: Package,
    ) -> Part: ...
