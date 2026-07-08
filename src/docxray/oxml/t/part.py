from functools import cached_property
from typing import Generic, Self

# docxray stuff
from docxray.opc.packuri import PackURI
from docxray.opc.part import XmlPart

from .package import TransitionalPackage
from .parser import parse_xml
from .types import ELM_T
from .xmlchemy import OxmlElement


class TransitionalPart(XmlPart[TransitionalPackage], Generic[ELM_T]):
    """Main part class for transitional (foollowed by ECMA-376, Part 1 and 4) parts in MS Word."""

    def __init__(
        self,
        partname: PackURI,
        content_type: str,
        element: ELM_T,
        blob: bytes | None = None,
        package: TransitionalPackage | None = None,
    ) -> None:
        super().__init__(partname, content_type, blob, package)
        self._element = element

    @cached_property
    def element(self) -> ELM_T:
        return self._element

    @classmethod
    def load(
        cls,
        partname: PackURI,
        content_type: str,
        blob: bytes,
        package: TransitionalPackage,
    ) -> Self:
        element = parse_xml(blob, OxmlElement)
        return cls(partname, content_type, element, package=package)  # type: ignore[arg-type]
