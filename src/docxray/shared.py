"""Objects shared by docx modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic

# docxray stuff
from docxray.types import ELM_T, ProvidesStoryPart, ProvidesXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart
    from docxray.parts.story import StoryPart


class ElementProxy(Generic[ELM_T]):
    """Base class for lxml element proxy classes.

    An element proxy class is one whose primary responsibilities are fulfilled by
    manipulating the attributes and child elements of an XML element. They are the most
    common type of class in python-docx other than custom element (oxml) classes.
    """

    def __init__(
        self, element: ELM_T, parent: ProvidesXmlPart[ELM_T] | None = None
    ) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self) -> XmlPart[ELM_T]:
        """The package part containing this object."""
        if self._parent is None:
            raise ValueError("part is not accessible from this element")
        return self._parent.part


class Parented(Generic[ELM_T]):
    """Provides common services for document elements that occur below a part but may
    occasionally require an ancestor object to provide a service, such as add or drop a
    relationship.

    Provides ``self._parent`` attribute to subclasses.
    """

    def __init__(self, parent: ProvidesXmlPart[ELM_T]) -> None:
        self._parent = parent

    @property
    def part(self) -> XmlPart[ELM_T]:
        """The package part containing this object."""
        return self._parent.part


class StoryChild(Generic[ELM_T]):
    """A document element within a story part.

    Story parts include DocumentPart and Header/FooterPart and can contain block items
    (paragraphs and tables). Items from the block-item subtree occasionally require an
    ancestor object to provide access to part-level or package-level items like styles
    or images or to add or drop a relationship.

    Provides `self._parent` attribute to subclasses.
    """

    def __init__(self, parent: ProvidesStoryPart[ELM_T]):
        self._parent = parent

    @property
    def part(self) -> StoryPart[ELM_T]:
        """The package part containing this object."""
        return self._parent.part
