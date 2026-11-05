from typing import Self

# docxray stuff
from docxray2.ns import MEDIA_TYPE
from docxray2.types import PkgFile

from .oxml import E_Default, E_Override, E_Types
from .part import Part
from .phys_pkg import PhysPkgWriter, phys_pkg_writer
from .pkg_uri import CONTENT_TYPES_PKG_URI, PKG_URI, PkgURI
from .rel import Relationships
from .spec import DEFAULT_CONTENT_TYPES


class PkgWriter:
    @staticmethod
    def write(
        pkg_file: PkgFile, rels: Relationships, parts: list[Part]
    ) -> None:
        phys_writer = phys_pkg_writer(pkg_file)
        PkgWriter._write_content_types(phys_writer, parts)
        PkgWriter._write_parts(phys_writer, parts)
        PkgWriter._write_rels(phys_writer, rels)
        phys_writer.close()

    @staticmethod
    def _write_content_types(
        phys_writer: PhysPkgWriter, parts: list[Part]
    ) -> None:
        cti = _ContentTypesItem.from_parts(parts)
        phys_writer.write(CONTENT_TYPES_PKG_URI, cti.blob)

    @staticmethod
    def _write_parts(phys_writer: PhysPkgWriter, parts: list[Part]) -> None:
        for part in parts:
            phys_writer.write(part.part_name, part.blob)
            if len(part.rels):
                phys_writer.write(part.part_name.rels_uri, part.rels.xml)

    @staticmethod
    def _write_rels(phys_writer: PhysPkgWriter, rels: Relationships) -> None:
        phys_writer.write(PKG_URI.rels_uri, rels.xml)


class _ContentTypesItem:
    def __init__(self) -> None:
        self._defaults: dict[str, str] = {}
        self._overrides: dict[str, str] = {}

    @property
    def blob(self) -> bytes:
        return self._element.to_string()

    @classmethod
    def from_parts(cls, parts: list[Part]) -> Self:
        cti = cls()
        cti._defaults["rels"] = MEDIA_TYPE.RELATIONSHIPS
        cti._defaults["xml"] = MEDIA_TYPE.XML
        for part in parts:
            cti._add_content_type(part.part_name, part.content_type)
        return cti

    def _add_content_type(self, part_name: PkgURI, content_type: str) -> None:
        ext = part_name.ext
        if (ext.lower(), content_type) in DEFAULT_CONTENT_TYPES:
            self._defaults[ext] = content_type
        else:
            self._overrides[part_name] = content_type

    @property
    def _element(self) -> E_Types:
        types_elm = E_Types.new(True)
        for ext in sorted(self._defaults.keys()):
            elm_default = E_Default.new(True)
            elm_default.Extension = ext
            elm_default.ContentType = self._defaults[ext]
            types_elm.append(elm_default)
        for part_name in sorted(self._overrides.keys()):
            elm_override = E_Override.new(True)
            elm_override.PartName = part_name
            elm_override.ContentType = self._overrides[part_name]
            types_elm.append(elm_override)
        return types_elm
