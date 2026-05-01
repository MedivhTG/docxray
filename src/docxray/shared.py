"""Objects shared by docx modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

# docxray stuff
from docxray.types import ELM_T

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart

XML_PART_T = TypeVar("XML_PART_T", bound="XmlPart")


class PartProxy(Generic[ELM_T, XML_PART_T]):
    def __init__(self, element: ELM_T, part: XML_PART_T | None = None) -> None:
        self._element = element
        self._part = part

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self) -> XML_PART_T:
        """The package part containing this object."""
        if self._part is None:
            raise ValueError("part is not accessible from this element")
        return self._part


PARENT_T = TypeVar("PARENT_T")


class ElementProxy(Generic[ELM_T, PARENT_T]):
    def __init__(self, element: ELM_T, parent: PARENT_T) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def parent(self) -> PARENT_T:
        return self._parent
