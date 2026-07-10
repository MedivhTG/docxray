from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.t.proxy.base import StoryChild
from docxray.oxml.t.text.hyperlink import CT_Hyperlink

if TYPE_CHECKING:
    from .paragraph import Paragraph, PContent


class Hyperlink(StoryChild[CT_Hyperlink]):
    @cached_property
    def paragraph(self) -> Paragraph:
        return cast("Paragraph", self._parent)

    @cached_property
    def raw_text(self) -> str:
        from .paragraph import p_raw_text

        return p_raw_text(self)

    def iter_inner_content(self) -> Iterator[PContent]:
        from .paragraph import p_content_iter

        return p_content_iter(self)
