from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

# docxray stuff
from docxray2.opc.part import Part
from docxray2.opc.pkg_uri import PkgURI
from docxray2.xmlchemy import BaseOxmlElement

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.opc.package import Package


class OpcPart(Part["Package"]):
    pass


class OpcXmlPart[ELM_T: BaseOxmlElement](OpcPart):
    ELEMENT: type[ELM_T]

    def __init__(
        self,
        part_name: PkgURI,
        content_type: str,
        element: ELM_T,
        blob: bytes | None = None,
        package: Package | None = None,
    ) -> None:
        super().__init__(part_name, content_type, blob, package)
        self._element = element

    @cached_property
    def element(self) -> ELM_T:
        return self._element

    @property
    def blob(self) -> bytes:
        return self.element.to_string()

    @property
    def _part(self) -> Self:
        return self

    @classmethod
    def load(
        cls,
        part_name: PkgURI,
        content_type: str,
        blob: bytes,
        package: Package,
    ) -> Self:
        element = cls.ELEMENT.from_xml(blob)
        return cls(part_name, content_type, element, package=package)
