from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.shared import Length, StoryChild
from docxray.oxml.trans.st.enums import (
    SE_JC,
    SE_LINE_SPACING_RULE,
    SE_TEXT_DIRECTION,
)
from docxray.oxml.trans.text.hyperlink import CT_Hyperlink
from docxray.oxml.trans.text.omath import CT_OMath, CT_OMathPara
from docxray.oxml.trans.text.paragraph import CT_P
from docxray.oxml.trans.text.run import CT_R

from .hyperlink import Hyperlink
from .omath import OMath, OMathParagraph
from .run import Run

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.paragraph_h2d import ParagraphH2D
    from docxray.oxml.trans.proxy.document import Body
    from docxray.oxml.trans.proxy.list import (
        ListItem,
        ListView,
        ListViewInterrupted,
    )
    from docxray.oxml.trans.proxy.table.cell import Cell
    from docxray.oxml.trans.proxy.table.table import Table

type ParaContentProxy = Run | Hyperlink | OMathParagraph | OMath


class Paragraph(StoryChild[CT_P]):
    @cached_property
    def h2d(self) -> ParagraphH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.paragraph_h2d import ParagraphH2D

        return ParagraphH2D(self, self.part.document_part, "pPr")

    @cached_property
    def container(self) -> Body | Cell:
        return cast("Body | Cell", self._parent)

    @cached_property
    def content_idx(self) -> int:
        return self.container.inner_content.index(self)

    @cached_property
    def prev_content_item(self) -> Paragraph | Table | None:
        prev_idx = self.content_idx - 1
        if prev_idx < 0:
            return None
        return self.container.inner_content[prev_idx]

    @cached_property
    def prev_para(self) -> Paragraph | None:
        prev_item = self.prev_content_item
        while prev_item:
            if isinstance(prev_item, Paragraph):
                return prev_item
            prev_item = prev_item.prev_content_item
        return None

    @cached_property
    def next_content_item(self) -> Paragraph | Table | None:
        next_idx = self.content_idx + 1
        if next_idx + 1 > len(self.container.inner_content):
            return None
        return self.container.inner_content[next_idx]

    @cached_property
    def next_para(self) -> Paragraph | None:
        next_item = self.next_content_item
        while next_item:
            if isinstance(next_item, Paragraph):
                return next_item
            next_item = next_item.next_content_item
        return None

    @cached_property
    def list_item(self) -> ListItem | None:
        return self.h2d.list_item

    @cached_property
    def list_view(self) -> ListView | None:
        return self.h2d.list_view

    @cached_property
    def list_view_interrupted(self) -> ListViewInterrupted | None:
        return self.h2d.list_view_interrupted

    @cached_property
    def right_to_left(self) -> bool:
        return self.h2d.right_to_left

    @cached_property
    def text_flow(self) -> SE_TEXT_DIRECTION | None:
        return self.h2d.text_flow

    @cached_property
    def margin_line_start(self) -> Length | int | None:
        return self.h2d.margin_line_start

    @cached_property
    def margin_line_end(self) -> Length | int | None:
        return self.h2d.margin_line_end

    @cached_property
    def text_indent(self) -> Length | int | None:
        return self.h2d.text_indent

    @cached_property
    def header_level(self) -> WD_HEADER_LEVEL:
        return self.h2d.header_level

    @cached_property
    def alignment(self) -> SE_JC:
        return self.h2d.alignment

    @cached_property
    def word_wrap(self) -> bool:
        return self.h2d.word_wrap

    @cached_property
    def justify_inter_character(self) -> bool:
        return self.h2d.justify_inter_character

    @cached_property
    def margin_top(self) -> Length | int | None:
        return self.h2d.margin_top

    @cached_property
    def margin_bottom(self) -> Length | int | None:
        return self.h2d.margin_bottom

    @cached_property
    def line_height(self) -> Length | int | None:
        return self.h2d.line_height

    @cached_property
    def line_rule(self) -> SE_LINE_SPACING_RULE:
        return self.h2d.line_rule

    @cached_property
    def page_break_before(self) -> bool:
        return self.h2d.page_break_before

    @cached_property
    def has_last_rendered_page_break(self) -> bool:
        return self.element.xpath("boolean(.//w:lastRenderedPageBreak)")

    @cached_property
    def has_page_break(self) -> bool:
        return self.element.xpath('boolean(.//w:br[@w:type="page"])')

    @cached_property
    def has_section_property(self) -> bool:
        return self.element.xpath("boolean(./w:pPr/w:sectPr)")

    @cached_property
    def has_text(self) -> bool:
        return self.element.xpath("boolean(.//w:t | .//m:t)")

    @cached_property
    def has_picture(self) -> bool:
        return self.element.xpath(
            "boolean(.//pic:pic/pic:blipFill/a:blip/@r:embed)"
        )

    @cached_property
    def raw_text(self) -> str:
        txt = ""
        for item in self.iter_inner_content():
            txt += item.raw_text
        return txt

    def iter_inner_content(
        self,
    ) -> Iterator[ParaContentProxy]:
        for item in self.element.inner_content_elements:
            if isinstance(item, CT_R):
                yield Run(item, self)
            elif isinstance(item, CT_Hyperlink):
                yield Hyperlink(item, self)
            elif isinstance(item, CT_OMathPara):
                yield OMathParagraph(item, self)
            elif isinstance(item, CT_OMath):
                yield OMath(item, self)
