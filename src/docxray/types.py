"""Abstract types used by `python-docx`."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, TypeVar

from typing_extensions import Protocol

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart
    from docxray.oxml.xmlchemy import OxmlElement
    from docxray.parts.story import StoryPart

ELM_T = TypeVar("ELM_T", bound="OxmlElement")


class ProvidesStoryPart(Protocol[ELM_T]):
    """An object that provides access to the StoryPart.

    This type is for objects that have a story part like document or header as their
    root part.
    """

    @property
    def part(self) -> StoryPart[ELM_T]: ...


class ProvidesXmlPart(Protocol[ELM_T]):
    """An object that provides access to its XmlPart.

    This type is for objects that need access to their part but it either isn't a
    StoryPart or they don't care, possibly because they just need access to the package
    or related parts.
    """

    @property
    def part(self) -> XmlPart[ELM_T]: ...


type PkgFile = str | Path | BinaryIO
