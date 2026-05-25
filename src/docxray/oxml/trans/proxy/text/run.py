from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import StoryChild
from docxray.oxml.trans.st.enums import SE_Underline, SE_VerticalAlignRun
from docxray.oxml.trans.text.run import CT_R

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.run import CharsCase, RunH2D

    from .paragraph import Paragraph


class Run(StoryChild[CT_R]):
    @cached_property
    def h2d(self) -> RunH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.run import RunH2D

        return RunH2D(self, self.part.document_part, "rPr")

    @cached_property
    def paragraph(self) -> Paragraph:
        return cast("Paragraph", self._parent)

    @cached_property
    def italic(self) -> bool:
        return self.h2d.italic

    @cached_property
    def bold(self) -> bool:
        return self.h2d.bold

    @cached_property
    def chars_case(self) -> CharsCase:
        return self.h2d.chars_case

    @cached_property
    def strike(self) -> bool:
        return self.h2d.single_strike_through

    @cached_property
    def underline(self) -> SE_Underline | None:
        return self.h2d.underline

    @cached_property
    def vertical_alignment(self) -> SE_VerticalAlignRun | None:
        return self.h2d.vertical_alignment
