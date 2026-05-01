"""Low-level, read-only API to a serialized Open Packaging Convention (OPC) package."""

from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property

# docxray stuff
from docxray.opc.constants import RELATIONSHIP_TARGET_MODE as RTM
from docxray.opc.oxml import (
    CT_Relationship,
    CT_Relationships,
    CT_Types,
    parse_xml,
)
from docxray.opc.packuri import PACKAGE_URI, PackURI
from docxray.opc.phys_pkg import PhysPkgReader, phys_pkg_reader
from docxray.opc.shared import CaseInsensitiveDict
from docxray.types import PkgFile


class PackageReader:
    """Provides access to the contents of a zip-format OPC package via its
    :attr:`serialized_parts` and :attr:`pkg_srels` attributes."""

    def __init__(
        self,
        content_types: _ContentTypeMap,
        pkg_srels: _SerializedRelationships,
        sparts: tuple[_SerializedPart, ...],
    ) -> None:
        self._content_types = content_types
        self._pkg_srels = pkg_srels
        self._sparts = sparts

    @staticmethod
    def from_file(pkg_file: PkgFile) -> PackageReader:
        """Return a |PackageReader| instance loaded with contents of `pkg_file`."""
        phys_reader = phys_pkg_reader(pkg_file)
        content_types = _ContentTypeMap.from_xml(phys_reader.content_types_xml)
        pkg_srels = PackageReader._srels_for(phys_reader, PACKAGE_URI)
        sparts = PackageReader._load_serialized_parts(
            phys_reader, pkg_srels, content_types
        )
        phys_reader.close()
        return PackageReader(content_types, pkg_srels, sparts)

    def iter_sparts(self) -> Iterator[tuple[PackURI, str, str, bytes]]:
        """Generate a 4-tuple `(partname, content_type, reltype, blob)` for each of the
        serialized parts in the package."""
        for s in self._sparts:
            yield (s.partname, s.content_type, s.reltype, s.blob)

    def iter_srels(self) -> Iterator[tuple[PackURI, _SerializedRelationship]]:
        """Generate a 2-tuple `(source_uri, srel)` for each of the relationships in the
        package."""
        for srel in self._pkg_srels:
            yield (PACKAGE_URI, srel)
        for spart in self._sparts:
            for srel in spart.srels:
                yield (spart.partname, srel)

    @staticmethod
    def _load_serialized_parts(
        phys_reader: PhysPkgReader,
        pkg_srels: _SerializedRelationships,
        content_types: _ContentTypeMap,
    ) -> tuple[_SerializedPart, ...]:
        """Return a list of |_SerializedPart| instances corresponding to the parts in
        `phys_reader` accessible by walking the relationship graph starting with
        `pkg_srels`."""
        sparts = []
        part_walker = PackageReader._walk_phys_parts(phys_reader, pkg_srels)
        for partname, blob, reltype, srels in part_walker:
            content_type = content_types[partname]
            spart = _SerializedPart(
                partname, content_type, reltype, blob, srels
            )
            sparts.append(spart)
        return tuple(sparts)

    @staticmethod
    def _srels_for(
        phys_reader: PhysPkgReader, source_uri: PackURI
    ) -> _SerializedRelationships:
        """Return |_SerializedRelationships| instance populated with relationships for
        source identified by `source_uri`."""
        rels_xml = phys_reader.rels_xml_for(source_uri)
        return _SerializedRelationships.load_from_xml(
            source_uri.baseURI, rels_xml
        )

    @staticmethod
    def _walk_phys_parts(
        phys_reader: PhysPkgReader,
        srels: _SerializedRelationships,
        visited_partnames: set[PackURI] | None = None,
    ) -> Iterator[tuple[PackURI, bytes, str, _SerializedRelationships]]:
        """Generate a 4-tuple `(partname, blob, reltype, srels)` for each of the parts
        in `phys_reader` by walking the relationship graph rooted at srels."""
        if visited_partnames is None:
            visited_partnames = set()
        for srel in srels:
            if srel.is_external:
                continue
            partname = srel.target_partname
            if partname in visited_partnames:
                continue
            visited_partnames.add(partname)
            reltype = srel.reltype
            part_srels = PackageReader._srels_for(phys_reader, partname)
            blob = phys_reader.blob_for(partname)
            yield (partname, blob, reltype, part_srels)
            yield from PackageReader._walk_phys_parts(
                phys_reader, part_srels, visited_partnames
            )


class _ContentTypeMap:
    """Value type providing dictionary semantics for looking up content type by part
    name, e.g. ``content_type = cti['/ppt/presentation.xml']``."""

    def __init__(self) -> None:
        self._overrides = CaseInsensitiveDict()
        self._defaults = CaseInsensitiveDict()

    def __getitem__(self, partname: PackURI) -> str:
        """Return content type for part identified by `partname`."""
        if partname in self._overrides:
            return self._overrides[partname]
        if partname.ext in self._defaults:
            return self._defaults[partname.ext]
        tmpl = "no content type for partname '%s' in [Content_Types].xml"
        raise KeyError(tmpl % partname)

    @staticmethod
    def from_xml(content_types_xml: bytes) -> _ContentTypeMap:
        """Return a new |_ContentTypeMap| instance populated with the contents of
        `content_types_xml`."""
        Types_elm = parse_xml(content_types_xml, CT_Types)
        ct_map = _ContentTypeMap()
        for o in Types_elm.overrides:
            ct_map._add_override(o.partname, o.content_type)
        for d in Types_elm.defaults:
            ct_map._add_default(d.extension, d.content_type)
        return ct_map

    def _add_default(self, extension: str, content_type: str) -> None:
        """Add the default mapping of `extension` to `content_type` to this content type
        mapping."""
        self._defaults[extension] = content_type

    def _add_override(self, partname: str, content_type: str) -> None:
        """Add the default mapping of `partname` to `content_type` to this content type
        mapping."""
        self._overrides[partname] = content_type


class _SerializedPart:
    """Value object for an OPC package part.

    Provides access to the partname, content type, blob, and serialized relationships
    for the part.
    """

    def __init__(
        self,
        partname: PackURI,
        content_type: str,
        reltype: str,
        blob: bytes,
        srels: _SerializedRelationships,
    ) -> None:
        self._partname = partname
        self._content_type = content_type
        self._reltype = reltype
        self._blob = blob
        self._srels = srels

    @property
    def partname(self) -> PackURI:
        return self._partname

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def blob(self) -> bytes:
        return self._blob

    @property
    def reltype(self) -> str:
        """The referring relationship type of this part."""
        return self._reltype

    @property
    def srels(self) -> _SerializedRelationships:
        return self._srels


class _SerializedRelationship:
    """Value object representing a serialized relationship in an OPC package.

    Serialized, in this case, means any target part is referred to via its partname
    rather than a direct link to an in-memory |Part| object.
    """

    def __init__(self, baseURI: str, Relationship_elm: CT_Relationship):
        self._baseURI = baseURI
        self._rId = Relationship_elm.rId
        self._reltype = Relationship_elm.reltype
        self._target_mode = Relationship_elm.target_mode
        self._target_ref = Relationship_elm.target_ref

    @property
    def is_external(self) -> bool:
        """True if target_mode is ``RTM.EXTERNAL``"""
        return self._target_mode == RTM.EXTERNAL

    @property
    def reltype(self) -> str:
        """Relationship type, like ``RT.OFFICE_DOCUMENT``"""
        return self._reltype

    @property
    def rId(self) -> str:
        """Relationship id, like 'rId9', corresponds to the ``Id`` attribute on the
        ``CT_Relationship`` element."""
        return self._rId

    @property
    def target_mode(self) -> str:
        """String in ``TargetMode`` attribute of ``CT_Relationship`` element, one of
        ``RTM.INTERNAL`` or ``RTM.EXTERNAL``."""
        return self._target_mode

    @property
    def target_ref(self) -> str:
        """String in ``Target`` attribute of ``CT_Relationship`` element, a relative
        part reference for internal target mode or an arbitrary URI, e.g. an HTTP URL,
        for external target mode."""
        return self._target_ref

    @cached_property
    def target_partname(self) -> PackURI:
        """|PackURI| instance containing partname targeted by this relationship.

        Raises ``ValueError`` on reference if target_mode is ``'External'``. Use
        :attr:`target_mode` to check before referencing.
        """
        if self.is_external:
            msg = (
                "target_partname attribute on Relationship is undefined w"
                'here TargetMode == "External"'
            )
            raise ValueError(msg)
        # lazy-load _target_partname attribute
        return PackURI.from_rel_ref(self._baseURI, self.target_ref)


class _SerializedRelationships:
    """Read-only sequence of |_SerializedRelationship| instances corresponding to the
    relationships item XML passed to constructor."""

    def __init__(self) -> None:
        self._srels: list[_SerializedRelationship] = []

    def __iter__(self) -> Iterator[_SerializedRelationship]:
        """Support iteration, e.g. 'for x in srels:'."""
        return self._srels.__iter__()

    @staticmethod
    def load_from_xml(
        baseURI: str, rels_item_xml: bytes | None
    ) -> _SerializedRelationships:
        """Return |_SerializedRelationships| instance loaded with the relationships
        contained in `rels_item_xml`.

        Returns an empty collection if `rels_item_xml` is |None|.
        """
        srels = _SerializedRelationships()
        if rels_item_xml is not None:
            Relationships_elm = parse_xml(rels_item_xml, CT_Relationships)
            for Relationship_elm in Relationships_elm.Relationship_lst:
                srels._srels.append(
                    _SerializedRelationship(baseURI, Relationship_elm)
                )
        return srels
