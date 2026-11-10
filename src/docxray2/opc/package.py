from collections.abc import Generator
from functools import cached_property
from typing import Self, TypeVar

# docxray stuff
from docxray2.types import PkgFile

from .part import Part
from .pkg_reader import PkgReader
from .pkg_uri import PKG_URI, PkgURI
from .pkg_writer import PkgWriter
from .rel import Relationship, Relationships
from .types import PartFactory

PART_T = TypeVar("PART_T", bound=Part)


class OpcPackage:
    @cached_property
    def rels(self) -> Relationships:
        return Relationships(PKG_URI.baseURI)

    @property
    def parts(self) -> list[Part]:
        return list(self.iter_parts())

    def save(self, pkg_file: PkgFile) -> None:
        parts = self.parts
        for part in parts:
            part.before_marshal()
        PkgWriter.write(pkg_file, self.rels, parts)

    def iter_parts(self) -> Generator[Part]:
        def walk_parts(
            source: OpcPackage | Part, visited: list[Part] | None = None
        ) -> Generator[Part]:
            for rel in source.rels.values():
                if visited is None:
                    visited = []
                if rel.external:
                    continue
                part = rel.target_part
                if part in visited:
                    continue
                visited.append(part)
                yield part
                new_source = part
                for part in walk_parts(new_source, visited):
                    yield part

        yield from walk_parts(self)

    def part_related_by(
        self, rel_type: str, part_type: type[PART_T] = Part  # type: ignore[assignment]
    ) -> PART_T | None:
        part = self.rels.part_with_rel_type(rel_type)
        if part is None:
            return None
        assert isinstance(part, part_type)
        return part

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
    def open(cls, pkg_file: PkgFile, part_factory: type[PartFactory]) -> Self:
        pkg_reader = PkgReader.from_file(pkg_file)
        package = cls()
        Unmarshaller.unmarshal(pkg_reader, package, part_factory)
        return package


class Unmarshaller:
    @classmethod
    def unmarshal(
        cls,
        pkg_reader: PkgReader,
        opc_package: OpcPackage,
        part_factory: type[PartFactory],
    ) -> None:
        parts = Unmarshaller._unmarshal_parts(
            pkg_reader, opc_package, part_factory
        )
        Unmarshaller._unmarshal_relationships(pkg_reader, opc_package, parts)
        for part in parts.values():
            part.after_unmarshal()
        opc_package.after_unmarshal()

    @classmethod
    def _unmarshal_parts(
        cls,
        pkg_reader: PkgReader,
        opc_package: OpcPackage,
        part_factory: type[PartFactory],
    ) -> dict[PkgURI, Part]:
        parts: dict[PkgURI, Part] = {}
        for (
            part_name,
            content_type,
            rel_type,
            blob,
        ) in pkg_reader.iter_sparts():
            parts[part_name] = part_factory.create_part(
                part_name, content_type, rel_type, blob, opc_package
            )
        return parts

    @classmethod
    def _unmarshal_relationships(
        cls,
        pkg_reader: PkgReader,
        opc_package: OpcPackage,
        parts: dict[PkgURI, Part],
    ) -> None:
        for source_uri, srel in pkg_reader.iter_srels():
            source = opc_package if source_uri == "/" else parts[source_uri]
            target = (
                srel.target_part
                if srel.is_external
                else parts.get(srel.target_part_name)
            )
            if target is None:
                continue
            source.load_rel(
                srel.rel_type, target, srel.rel_id, srel.is_external
            )
