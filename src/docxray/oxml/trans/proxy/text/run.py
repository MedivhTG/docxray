from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.shared import ElementProxy, StoryChild
from docxray.oxml.trans.shared import CT_Empty
from docxray.oxml.trans.st.enums import (
    SE_BR_CLEAR,
    SE_BR_TYPE,
    SE_Underline,
    SE_VerticalAlignRun,
)
from docxray.oxml.trans.text.run import CT_R, CT_Br, CT_PTab, CT_Text

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.run import CharsCase, RunH2D

    from .paragraph import Paragraph


class Tab(ElementProxy[CT_Empty]):
    pass


class Break(ElementProxy[CT_Br]):
    @cached_property
    def which_break(self) -> SE_BR_TYPE:
        if self.element.type is None:
            return SE_BR_TYPE.TEXT_WRAPPING
        return self.element.type

    @cached_property
    def how_wrap(self) -> SE_BR_CLEAR:
        if self.which_break != SE_BR_TYPE.TEXT_WRAPPING:
            return SE_BR_CLEAR.NONE
        if self.element.clear_attr is None:
            return SE_BR_CLEAR.NONE
        return self.element.clear_attr


class TxtFragment(ElementProxy[CT_Text]):
    @cached_property
    def raw(self) -> str:
        return self._element.txt

    @cached_property
    def preserve(self) -> bool:
        return self.element.space == "preserve"


class Run(StoryChild[CT_R]):
    @cached_property
    def h2d(self) -> RunH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.run import RunH2D

        return RunH2D(self, self.part.document_part, "rPr")

    @cached_property
    def paragraph(self) -> Paragraph:
        from .hyperlink import Hyperlink
        from .paragraph import Paragraph

        if isinstance(self._parent, Paragraph):
            return self._parent
        elif isinstance(self._parent, Hyperlink):
            return self._parent.paragraph
        return cast(Paragraph, self._parent)

    @cached_property
    def italic(self) -> bool:
        return self.h2d.italic

    @cached_property
    def bold(self) -> bool:
        return self.h2d.bold

    @cached_property
    def chars_case(self) -> CharsCase | None:
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

    def iter_inner_content(
        self,
    ) -> Iterator[TxtFragment | Drawing | Break | Tab]:
        for item in self.element.inner_content_items:
            if isinstance(item, CT_Text):
                yield TxtFragment(item, self)
            elif isinstance(item, CT_Drawing):
                yield Drawing(item, self)
            elif isinstance(item, CT_Br):
                yield Break(item, self)
            # TODO: extend
            elif isinstance(item, CT_PTab):
                continue
            # TODO: extend
            elif isinstance(item, CT_Empty):
                if item.tag == W.TAB:
                    yield Tab(item, self)
