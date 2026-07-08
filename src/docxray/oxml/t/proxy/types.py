"""Abstract types used by `docxray`."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart
    from docxray.oxml.t.parts.story import StoryPart


class ProvidesStoryPart(Protocol):
    """An object that provides access to the StoryPart.

    This type is for objects that have a story part like document or header as their
    root part.
    """

    @cached_property
    def part(self) -> StoryPart: ...


class ProvidesXmlPart(Protocol):
    """An object that provides access to its XmlPart.

    This type is for objects that need access to their part but it either isn't a
    StoryPart or they don't care, possibly because they just need access to the package
    or related parts.
    """

    @cached_property
    def part(self) -> XmlPart: ...
