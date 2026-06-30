from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.shared import ElementProxy, StoryChild
from docxray.oxml.trans.shared import CT_Empty
from docxray.oxml.trans.st.enums import (
    SE_BR_CLEAR,
    SE_BR_TYPE,
    SE_UNDERLINE,
    SE_VerticalAlignRun,
)
from docxray.oxml.trans.text.run import (
    CT_R,
    CT_Br,
    CT_PTab,
    CT_Text,
    RunInnerContent,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.run_h2d import CharsCase, RunH2D

    from .paragraph import Paragraph

type RunContentProxy = TxtFragment | Drawing | Break | Tab


def run_content(
    item: RunInnerContent, instance: Any
) -> RunContentProxy | None:
    if isinstance(item, CT_Text):
        return TxtFragment(item, instance)
    elif isinstance(item, CT_Drawing):
        return Drawing(item, instance)
    elif isinstance(item, CT_Br):
        return Break(item, instance)
    # TODO: extend
    elif isinstance(item, CT_PTab):
        return None
    # TODO: extend
    elif isinstance(item, CT_Empty):
        if item.tag == W.TAB:
            return Tab(item, instance)
    return None


class Tab(ElementProxy[CT_Empty]):
    pass


class Break(ElementProxy[CT_Br]):
    @cached_property
    def break_type(self) -> SE_BR_TYPE:
        if self.element.type is None:
            return SE_BR_TYPE.TEXT_WRAPPING
        return self.element.type

    @cached_property
    def how_wrap(self) -> SE_BR_CLEAR:
        if self.break_type != SE_BR_TYPE.TEXT_WRAPPING:
            return SE_BR_CLEAR.NONE
        if self.element.clear_attr is None:
            return SE_BR_CLEAR.NONE
        return self.element.clear_attr


class TxtFragment(ElementProxy[CT_Text]):
    @cached_property
    def raw(self) -> str:
        """Text inside of txt tag `as-is`."""
        return self._element.txt

    @cached_property
    def preserve(self) -> bool:
        """Preserve space chars inside of txt tag or not."""
        return self.element.space == "preserve"


class Run(StoryChild[CT_R]):
    @cached_property
    def h2d(self) -> RunH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.run_h2d import RunH2D

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
    def underline(self) -> SE_UNDERLINE | None:
        return self.h2d.underline

    @cached_property
    def vertical_alignment(self) -> SE_VerticalAlignRun | None:
        return self.h2d.vertical_alignment

    @cached_property
    def raw_text(self) -> str:
        txt = ""
        for item in self.iter_inner_content():
            if isinstance(item, TxtFragment):
                txt += item.raw
        return txt

    def iter_inner_content(
        self,
    ) -> Iterator[RunContentProxy]:
        for item in self.element.inner_content_items:
            proxy = run_content(item, self)
            if proxy:
                yield proxy
