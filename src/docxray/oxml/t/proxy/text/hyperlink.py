from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.t.proxy.base import StoryChild
from docxray.oxml.t.proxy.text.run import Run
from docxray.oxml.t.text.hyperlink import CT_Hyperlink
from docxray.oxml.t.text.run import CT_R

if TYPE_CHECKING:
    from .paragraph import Paragraph


class Hyperlink(StoryChild[CT_Hyperlink]):
    @cached_property
    def paragraph(self) -> Paragraph:
        return cast("Paragraph", self._parent)

    @cached_property
    def raw_text(self) -> str:
        txt = ""
        for run in self.iter_inner_content():
            txt += run.raw_text
        return txt

    def iter_inner_content(self) -> Iterator[Run]:
        for item in self.element.inner_content_elements:
            if isinstance(item, CT_R):
                yield Run(item, self)
