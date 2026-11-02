from functools import cached_property
from typing import Self

# docxray stuff
from docxray2.types import PkgFile

from .part import Part, PartFactory
from .pkg_reader import PkgReader
from .pkg_uri import PKG_URI, PkgURI
from .rel import Relationship, Relationships


class OpcPackage:
    @classmethod
    def open(cls, pkg_file: PkgFile, part_factory: type[PartFactory]) -> Self:
        pkg_reader = PkgReader.from_file(pkg_file)
        package = cls()
        Unmarshaller.unmarshal(pkg_reader, package, part_factory)
        return package

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

    @cached_property
    def rels(self) -> Relationships:
        return Relationships(PKG_URI.baseURI)


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
