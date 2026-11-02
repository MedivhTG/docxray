from __future__ import annotations

from collections.abc import Generator, Iterator
from dataclasses import dataclass
from warnings import warn

# docxray stuff
from docxray2.types import PkgFile

from .enums import SE_TARGET_MODE
from .oxml import E_Relationships, E_Types
from .phys_pkg_reader import PhysPkgReader, phys_pkg_reader
from .pkg_uri import PKG_URI, PkgURI


class PkgReader:
    def __init__(
        self,
        ct_map: _ContentTypeMap,
        srels: _SerializedRelationships,
        sparts: tuple[_SerializedPart, ...],
    ) -> None:
        self._ct_map = ct_map
        self._srels = srels
        self._sparts = sparts

    @staticmethod
    def from_file(pkg_file: PkgFile) -> PkgReader:
        phys_reader = phys_pkg_reader(pkg_file)
        ct_map = _ContentTypeMap.from_xml(phys_reader.content_types_xml)
        pkg_srels = PkgReader._srels_for(phys_reader, PKG_URI)
        pkg_sparts = PkgReader._load_serialized_parts(
            phys_reader, pkg_srels, ct_map
        )
        phys_reader.close()
        return PkgReader(ct_map, pkg_srels, pkg_sparts)

    @staticmethod
    def _srels_for(
        phys_reader: PhysPkgReader, source_uri: PkgURI
    ) -> _SerializedRelationships:
        rels_xml = phys_reader.rels_xml_for(source_uri)
        return _SerializedRelationships.load_from_xml(
            source_uri.baseURI, rels_xml
        )

    @staticmethod
    def _load_serialized_parts(
        phys_reader: PhysPkgReader,
        pkg_srels: _SerializedRelationships,
        ct_map: _ContentTypeMap,
    ) -> tuple[_SerializedPart, ...]:
        sparts = []
        part_walker = PkgReader._walk_phys_parts(phys_reader, pkg_srels)
        for part_name, blob, rel_type, part_srels in part_walker:
            content_type = ct_map[part_name]
            spart = _SerializedPart(
                part_name, content_type, rel_type, blob, part_srels
            )
            sparts.append(spart)
        return tuple(sparts)

    @staticmethod
    def _walk_phys_parts(
        phys_reader: PhysPkgReader,
        srels: _SerializedRelationships,
        visited_part_names: set[PkgURI] | None = None,
    ) -> Generator[tuple[PkgURI, bytes, str, _SerializedRelationships]]:
        if visited_part_names is None:
            visited_part_names = set()
        for srel in srels:
            if srel.is_external:
                continue
            part_name = srel.target_part_name
            if part_name in visited_part_names:
                continue
            visited_part_names.add(part_name)
            if not phys_reader.exists(part_name):
                srels.drop(srel)
                warn(
                    "Realationship missing in the package for: "
                    f"rId={srel.rel_id}, partname={part_name}",
                    stacklevel=2,
                )
                continue
            blob = phys_reader.blob_for(part_name)
            part_srels = PkgReader._srels_for(phys_reader, part_name)
            yield (part_name, blob, srel.rel_type, part_srels)
            yield from PkgReader._walk_phys_parts(
                phys_reader, part_srels, visited_part_names
            )


class _ContentTypeMap:
    def __init__(self) -> None:
        self._overrides: dict[str, str] = {}
        self._defaults: dict[str, str] = {}

    def __getitem__(self, part_name: PkgURI) -> str:
        if part_name in self._overrides:
            return self._overrides[part_name]
        if part_name.ext in self._defaults:
            return self._defaults[part_name.ext]
        raise KeyError(
            f"No content type for part_name {part_name} in [Content_Types].xml"
        )

    @staticmethod
    def from_xml(content_types_xml: bytes) -> _ContentTypeMap:
        types_elm = E_Types.from_xml(content_types_xml)
        ct_map = _ContentTypeMap()
        for override_elm in types_elm.overrides:
            ct_map._add_override(
                override_elm.part_name, override_elm.content_type
            )
        for default_elm in types_elm.defaults:
            ct_map._add_default(
                default_elm.extension, default_elm.content_type
            )
        return ct_map

    def _add_default(self, extension: str, content_type: str) -> None:
        self._defaults[extension] = content_type

    def _add_override(self, part_name: str, content_type: str) -> None:
        self._overrides[part_name] = content_type


@dataclass
class _SerializedPart:
    part_name: PkgURI
    content_type: str
    rel_type: str
    blob: bytes
    srels: _SerializedRelationships


@dataclass
class _SerializedRelationship:
    baseURI: str
    rel_id: str
    rel_type: str
    target_mode: SE_TARGET_MODE
    target_part: str

    @property
    def is_external(self) -> bool:
        return self.target_mode == SE_TARGET_MODE.EXTERNAL

    @property
    def target_part_name(self) -> PkgURI:
        if self.is_external:
            raise ValueError("Target part must be in TargetMode `Internal`")
        return PkgURI.from_rel_ref(self.baseURI, self.target_part)


class _SerializedRelationships:
    def __init__(self) -> None:
        self._srels: list[_SerializedRelationship] = []

    def __iter__(self) -> Iterator[_SerializedRelationship]:
        return self._srels.__iter__()

    def append(self, srel: _SerializedRelationship) -> None:
        self._srels.append(srel)

    def drop(self, srel: _SerializedRelationship) -> None:
        self._srels.remove(srel)

    @staticmethod
    def load_from_xml(
        baseURI: str, rels_item_xml: bytes | None
    ) -> _SerializedRelationships:
        srels = _SerializedRelationships()
        if rels_item_xml is not None:
            relationships_elm = E_Relationships.from_xml(rels_item_xml)
            for relationship_elm in relationships_elm.relationships:
                srels.append(
                    _SerializedRelationship(
                        baseURI,
                        relationship_elm.rel_id,
                        relationship_elm.rel_type,
                        relationship_elm.target_mode
                        or SE_TARGET_MODE.INTERNAL,
                        relationship_elm.target_part,
                    )
                )
        return srels
