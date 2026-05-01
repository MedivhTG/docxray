"""Objects that implement reading and writing OPC packages."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Iterator, TypeVar

# docxray stuff
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.opc.packuri import PACKAGE_URI, PackURI
from docxray.opc.part import PartFactory
from docxray.opc.pkgreader import PackageReader
from docxray.opc.rel import Relationships
from docxray.parts.document import DocumentPart
from docxray.types import PkgFile

if TYPE_CHECKING:
    from typing_extensions import Self

    # docxray stuff
    from docxray.opc.part import Part
    from docxray.opc.rel import _Relationship

PART_T = TypeVar("PART_T", bound="Part")


class OpcPackage:
    """Main API class for |python-opc|.

    A new instance is constructed by calling the :meth:`open` class method with a path
    to a package file or file-like object containing one.
    """

    def after_unmarshal(self) -> None:
        """Entry point for any post-unmarshaling processing.

        May be overridden by subclasses without forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    def iter_rels(self) -> Iterator[_Relationship]:
        """Generate exactly one reference to each relationship in the package by
        performing a depth-first traversal of the rels graph."""

        def walk_rels(
            source: OpcPackage | Part, visited: set[Part] | None = None
        ) -> Iterator[_Relationship]:
            visited = set() if visited is None else visited
            for rel in source.rels.values():
                yield rel
                if rel.is_external:
                    continue
                part = rel.target_part
                if part in visited:
                    continue
                visited.add(part)
                new_source = part
                yield from walk_rels(new_source, visited)

        yield from walk_rels(self)

    def iter_parts(self) -> Iterator[Part]:
        """Generate exactly one reference to each of the parts in the package by
        performing a depth-first traversal of the rels graph."""

        def walk_parts(
            source: Self | Part, visited: set[Part] | None = None
        ) -> Iterator[Part]:
            visited = set() if visited is None else visited
            for rel in source.rels.values():
                if rel.is_external:
                    continue
                part = rel.target_part
                if part in visited:
                    continue
                visited.add(part)
                yield part
                new_source = part
                yield from walk_parts(new_source, visited)

        yield from walk_parts(self)

    def load_rel(
        self,
        reltype: str,
        target: Part | str,
        rId: str,
        is_external: bool = False,
    ) -> _Relationship:
        """Return newly added |_Relationship| instance of `reltype` between this part
        and `target` with key `rId`.

        Target mode is set to ``RTM.EXTERNAL`` if `is_external` is |True|. Intended for
        use during load from a serialized package, where the rId is well known. Other
        methods exist for adding a new relationship to the package during processing.
        """
        return self.rels.add_relationship(reltype, target, rId, is_external)

    @property
    def main_document_part(self) -> DocumentPart:
        """Return a reference to the main document part for this package.

        Examples include a document part for a WordprocessingML package, a presentation
        part for a PresentationML package, or a workbook part for a SpreadsheetML
        package.
        """
        return self.part_related_by(RT.OFFICE_DOCUMENT, DocumentPart)

    @classmethod
    def open(cls, pkg_file: PkgFile) -> Self:
        """Return an |OpcPackage| instance loaded with the contents of `pkg_file`."""
        pkg_reader = PackageReader.from_file(pkg_file)
        package = cls()
        Unmarshaller.unmarshal(pkg_reader, package, PartFactory)
        return package

    def part_related_by(
        self, reltype: str, assert_part: type[PART_T]
    ) -> PART_T:
        """Return part to which this package has a relationship of `reltype`.

        Raises |KeyError| if no such relationship is found and |ValueError| if more than
        one such relationship is found.
        """
        part = self.rels.part_with_reltype(reltype)
        assert isinstance(part, assert_part)
        return part

    @property
    def parts(self) -> list[Part]:
        """Return a list containing a reference to each of the parts in this package."""
        return list(self.iter_parts())

    @cached_property
    def rels(self) -> Relationships:
        """Return a reference to the |Relationships| instance holding the collection of
        relationships for this package."""
        return Relationships(PACKAGE_URI.baseURI)


class Unmarshaller:
    """Hosts static methods for unmarshalling a package from a |PackageReader|."""

    @staticmethod
    def unmarshal(
        pkg_reader: PackageReader,
        package: OpcPackage,
        part_factory: type[PartFactory],
    ) -> None:
        """Construct graph of parts and realized relationships based on the contents of
        `pkg_reader`, delegating construction of each part to `part_factory`.

        Package relationships are added to `pkg`.
        """
        parts = Unmarshaller._unmarshal_parts(
            pkg_reader, package, part_factory
        )
        Unmarshaller._unmarshal_relationships(pkg_reader, package, parts)
        for part in parts.values():
            part.after_unmarshal()
        package.after_unmarshal()

    @staticmethod
    def _unmarshal_parts(
        pkg_reader: PackageReader,
        package: OpcPackage,
        part_factory: type[PartFactory],
    ) -> dict[PackURI, Part]:
        """Return a dictionary of |Part| instances unmarshalled from `pkg_reader`, keyed
        by partname.

        Side-effect is that each part in `pkg_reader` is constructed using
        `part_factory`.
        """
        parts: dict[PackURI, Part] = {}
        for partname, content_type, reltype, blob in pkg_reader.iter_sparts():
            parts[partname] = part_factory.create_part(
                partname, content_type, reltype, blob, package
            )

        return parts

    @staticmethod
    def _unmarshal_relationships(
        pkg_reader: PackageReader,
        package: OpcPackage,
        parts: dict[PackURI, Part],
    ) -> None:
        """Add a relationship to the source object corresponding to each of the
        relationships in `pkg_reader` with its target_part set to the actual target part
        in `parts`."""
        for source_uri, srel in pkg_reader.iter_srels():
            source = package if source_uri == "/" else parts[source_uri]
            target = (
                srel.target_ref
                if srel.is_external
                else parts[srel.target_partname]
            )
            source.load_rel(srel.reltype, target, srel.rId, srel.is_external)
