from __future__ import annotations

from ..types import PkgFile
from .oxml import E_Relationships, E_Types
from .phys_pkg_reader import PhysPkgReader, phys_pkg_reader
from .pkg_uri import PKG_URI, PkgURI


class PkgReader:
    @staticmethod
    def from_file(pkg_file: PkgFile) -> PkgReader:
        phys_reader = phys_pkg_reader(pkg_file)
        ct_map = _ContentTypeMap.from_xml(phys_reader.content_types_xml)
        srels = PkgReader._srels_for(phys_reader, PKG_URI)
        phys_reader.close()
        return PkgReader()

    @staticmethod
    def _srels_for(
        phys_reader: PhysPkgReader, source_uri: PkgURI
    ) -> _SerializedRelationships:
        rels_xml = phys_reader.rels_xml_for(source_uri)
        return _SerializedRelationships.load_from_xml(
            source_uri.baseURI, rels_xml
        )


class _ContentTypeMap:
    def __init__(self) -> None:
        self._overrides: dict[str, str] = {}
        self._defaults: dict[str, str] = {}

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


class _SerializedRelationships:
    @staticmethod
    def load_from_xml(
        baseURI: str, rels_item_xml: bytes | None
    ) -> _SerializedRelationships:
        srels = _SerializedRelationships()
        if rels_item_xml is not None:
            relationships_elm = E_Relationships.from_xml(rels_item_xml)
        return srels
