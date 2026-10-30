from __future__ import annotations

from ..types import PkgFile
from .oxml import E_Types
from .phys_pkg_reader import PhysPkgReader, phys_pkg_reader
from .pkg_uri import PkgURI


class PkgReader:
    @staticmethod
    def from_file(pkg_file: PkgFile) -> PkgReader:
        phys_reader = phys_pkg_reader(pkg_file)
        # ct_map = _ContentTypeMap.from_xml(phys_reader.content_types_xml)
        phys_reader.close()
        return PkgReader()

    @staticmethod
    def _srels_for(phys_reader: PhysPkgReader, source_uri: PkgURI):
        pass


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
