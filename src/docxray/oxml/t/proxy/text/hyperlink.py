from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.opc.constants import RELATIONSHIP_TYPE
from docxray.oxml.t.proxy.base import StoryChild
from docxray.oxml.t.proxy.compute import on_off
from docxray.oxml.t.text.hyperlink import CT_Hyperlink

if TYPE_CHECKING:
    from .paragraph import Paragraph, PContent

_FRAME_WINDOWS_VALS = {"_top", "_self", "_parent", "_blank"}


class Hyperlink(StoryChild[CT_Hyperlink]):
    @cached_property
    def paragraph(self) -> Paragraph:
        return cast("Paragraph", self._parent)

    # TODO: look for bookmarks and docs
    @cached_property
    def linked_to(self) -> str | None:
        """Get URI or object in Document (not implemented).

        Examples:
            1. MAIL -> `mailto:robots@gmail.com?subject=NO_SUBJECT`
            2. URL -> `https://www.google.com`
            3. PATH (relative) -> `abc.docx`

        Returns:
            str | None: URI for `str` or `None` if no valid reference.
        """

        rel_id = self.element.id
        if rel_id:
            rel = self.document_part.rels.get(rel_id)
            if rel is None:
                return None
            if rel.reltype != RELATIONSHIP_TYPE.HYPERLINK:
                return None
            return rel.target_ref
        bookmark_ref = self.element.anchor
        if bookmark_ref:
            return None
        external_ref = self.element.docLocation
        if external_ref:
            return None
        return None

    # TODO: frameset logic?
    @cached_property
    def target_frame(self) -> str | None:
        """Tells hot to open link for the current frame.

        Here can be values:
            1. `_top` - Open hyperlink target in the full region of the current window
            2. `_self` - Open hyperlink target in the same frame as the hyperlink appears
            3. `_parent` - Open hyperlink target in the parent of the current frame,
            or the current frame if this frame has no parent
            4. `_blank` - Open hyperlink target in a new web browser window
            5. all other values - Open hyperlink target in the frame with the specified
            name. If no frame exists with this name, open in the current frame
        """
        tgt = self.element.tgtFrame
        if not tgt:
            return None
        if tgt in _FRAME_WINDOWS_VALS:
            return tgt
        if tgt[0].isalpha():
            return tgt
        return None

    @cached_property
    def tooltip(self) -> str | None:
        """Shown hyperlink title."""
        return self.element.tooltip

    @cached_property
    def clicked(self) -> bool:
        """Tells if hyperlink is followed."""
        if self.element.history is None:
            return False
        return on_off(self.element.history)

    @cached_property
    def raw_text(self) -> str:
        from .paragraph import p_raw_text

        return p_raw_text(self)

    def iter_inner_content(self) -> Iterator[PContent]:
        from .paragraph import p_content_iter

        return p_content_iter(self)
