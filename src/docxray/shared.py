"""Objects shared by docx modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic

# docxray stuff
from docxray.parts.story import StoryPart
from docxray.types import ELM_T, ProvidesStoryPart, ProvidesXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart


class ElementProxy(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesXmlPart) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self) -> XmlPart:
        return self._parent.part


class StoryChild(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesStoryPart) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        return self._element

    @property
    def part(self) -> StoryPart:
        """The package part containing this object."""
        return self._parent.part
