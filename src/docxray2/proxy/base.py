from functools import cached_property

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.parts.base import DocxXmlPart
from docxray2.parts.types import ProvidesDocxXmlPart


class DocxElementProxy[ELM_T: Oxml, PART_T: DocxXmlPart = DocxXmlPart[ELM_T]]:
    def __init__(self, element: ELM_T, parent: ProvidesDocxXmlPart) -> None:
        self._element = element
        self._parent = parent

    @cached_property
    def part(self) -> PART_T:
        return self._part  # type: ignore[return-value]

    @cached_property
    def parent(self) -> ProvidesDocxXmlPart:
        return self._parent

    @property
    def element(self) -> ELM_T:
        return self._element

    @cached_property
    def _part(self) -> DocxXmlPart[ELM_T]:
        return self._parent._part
