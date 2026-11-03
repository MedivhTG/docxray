from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
import docxray2.parts as p

from .ns import MEDIA_TYPE
from .opc.part import Part
from .opc.pkg_uri import PkgURI

if TYPE_CHECKING:
    from .opc.package import OpcPackage


class DocxPartFactory:
    DEFAULT_PART_TYPE = Part

    part_type_for: dict[str, type[Part]] = {}

    @classmethod
    def create_part(
        cls,
        part_name: PkgURI,
        content_type: str,
        rel_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Part:
        PartClass = cls._part_cls_for(content_type)
        return PartClass.load(part_name, content_type, blob, package)

    @classmethod
    def _part_cls_for(cls, content_type: str) -> type[Part]:
        return cls.part_type_for.get(content_type, cls.DEFAULT_PART_TYPE)


DocxPartFactory.part_type_for[MEDIA_TYPE.CORE_PROPERTIES] = (
    p.CorePropertiesPart
)
DocxPartFactory.part_type_for[MEDIA_TYPE.MAIN_DOCUMENT] = p.MainDocumentPart
DocxPartFactory.part_type_for[MEDIA_TYPE.EXTENDED_FILE_PROPERTIES] = (
    p.ExtendedFilePropertiesPart
)
