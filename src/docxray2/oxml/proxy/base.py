from functools import cached_property

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.parts.types import ProvidesXmlPart
from docxray2.parts.xml import XmlPart


class ElementProxy[ELM_T: Oxml]:
    def __init__(self, element: ELM_T, parent: ProvidesXmlPart) -> None:
        self._element = element
        self._parent = parent

    @cached_property
    def part(self) -> XmlPart[ELM_T]:
        return self._parent.part

    @cached_property
    def element(self) -> ELM_T:
        return self._element
