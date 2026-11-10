from functools import cached_property

# docxray stuff
from docxray2.opc.oxml.parser import OpcOxml
from docxray2.opc.parts.base import OpcXmlPart
from docxray2.opc.parts.types import ProvidesOpcXmlPart


class OpcElementProxy[ELM_T: OpcOxml, PART_T: OpcXmlPart = OpcXmlPart[ELM_T]]:
    def __init__(self, element: ELM_T, parent: ProvidesOpcXmlPart) -> None:
        self._element = element
        self._parent = parent

    @cached_property
    def part(self) -> PART_T:
        return self._part  # type: ignore[return-value]

    @cached_property
    def parent(self) -> ProvidesOpcXmlPart:
        return self._parent

    @cached_property
    def element(self) -> ELM_T:
        return self._element

    @cached_property
    def _part(self) -> OpcXmlPart[ELM_T]:
        return self._parent._part
