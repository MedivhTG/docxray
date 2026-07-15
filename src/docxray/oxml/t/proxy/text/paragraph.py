from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, cast

# docxray stuff
from docxray.length import Length
from docxray.oxml.t.enums import WD_HEADER_LEVEL
from docxray.oxml.t.proxy.base import (
    NotFound,
    StoryChild,
    from_doc_dflts,
    from_style_inheritance,
)
from docxray.oxml.t.proxy.compute import (
    on_off,
    signed_twips_measure,
    twips_measure,
)
from docxray.oxml.t.proxy.numbering.numbering import Level
from docxray.oxml.t.proxy.styles.style import ParagraphStyle
from docxray.oxml.t.st.enums import (
    SE_JC,
    SE_LINE_SPACING_RULE,
    SE_STYLE_TYPE,
    SE_TEXT_ALIGNMENT,
    SE_TEXT_DIRECTION,
)
from docxray.oxml.t.text.hyperlink import CT_Hyperlink
from docxray.oxml.t.text.num_props import CT_NumPr
from docxray.oxml.t.text.omath import CT_OMath, CT_OMathPara
from docxray.oxml.t.text.paragraph import CT_P
from docxray.oxml.t.text.run import CT_R

from .hyperlink import Hyperlink
from .omath import OMath, OMathParagraph
from .run import Run

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.document import Body
    from docxray.oxml.t.proxy.table.cell import Cell
    from docxray.oxml.t.proxy.table.table import Table
    from docxray.oxml.t.proxy.text.list import (
        ListItem,
        ListView,
        ListViewInterrupted,
    )

type PContent = Run | Hyperlink | OMathParagraph | OMath
type _RslvOrder = Literal[
    "numbering_first", "paragraph_first", "up_to_hierarchy"
]


def p_content_iter(proxy: Paragraph | Hyperlink) -> Iterator[PContent]:
    for item in proxy.element.inner_content_elements:
        if isinstance(item, CT_R):
            yield Run(item, proxy)
        elif isinstance(item, CT_Hyperlink):
            yield Hyperlink(item, proxy)
        elif isinstance(item, CT_OMathPara):
            yield OMathParagraph(item, proxy)
        elif isinstance(item, CT_OMath):
            yield OMath(item, proxy)


def p_raw_text(proxy: Paragraph | Hyperlink) -> str:
    txt = ""
    for item in proxy.iter_inner_content():
        txt += item.raw_text
    return txt


class Paragraph(StoryChild[CT_P]):
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
        # docxray stuff
        from docxray.oxml.t.proxy.text.list import ListItem

        if self.document_part.numbering is None:
            return None
        if self._assoc_numPr is None:
            return None
        if self._assoc_lvl is None:
            return None
        return ListItem(
            self.document_part.numbering,
            self,
            self._assoc_numPr,
            self._assoc_lvl,
        )

    @cached_property
    def list_view(self) -> ListView | None:
        # docxray stuff
        from docxray.oxml.t.proxy.text.list import ListView

        if self.list_item is None:
            return None
        return ListView(self.list_item)

    @cached_property
    def list_view_interrupted(self) -> ListViewInterrupted | None:
        # docxray stuff
        from docxray.oxml.t.proxy.text.list import ListViewInterrupted

        if self.list_item is None:
            return None
        return ListViewInterrupted(self.list_item)

    @cached_property
    def right_to_left(self) -> bool:
        return on_off(self._display("pPr.bidi.val", True))

    # TODO: inherit from parent Section if omitted
    @cached_property
    def text_flow(self) -> SE_TEXT_DIRECTION | None:
        dir = self._display("pPr.textDirection.val")
        if isinstance(dir, NotFound):
            return None
        return dir

    @cached_property
    def margin_line_start(self) -> Length | int | None:
        left_chars: int | NotFound = self._display("pPr.ind.leftChars")
        if isinstance(left_chars, NotFound):
            left_chars = self._display("pPr.ind.startChars")
        if isinstance(left_chars, NotFound):
            left: int | str | NotFound = self._display("pPr.ind.left")
            if isinstance(left, NotFound):
                left = self._display("pPr.ind.start")
            if not isinstance(left, NotFound):
                return signed_twips_measure(left)
        else:
            return left_chars
        return None

    @cached_property
    def margin_line_end(self) -> Length | int | None:
        right_chars: int | NotFound = self._display("pPr.ind.rightChars")
        if isinstance(right_chars, NotFound):
            right_chars = self._display("pPr.ind.endChars")
        if isinstance(right_chars, NotFound):
            right: int | str | NotFound = self._display("pPr.ind.right")
            if isinstance(right, NotFound):
                right = self._display("pPr.ind.end")
            if not isinstance(right, NotFound):
                return signed_twips_measure(right)
        else:
            return right_chars
        return None

    @cached_property
    def text_indent(self) -> Length | int | None:
        text_indent = None
        hanging_chars: int | NotFound = self._display("pPr.ind.hangingChars")
        if not isinstance(hanging_chars, NotFound):
            text_indent = (
                hanging_chars if hanging_chars < 0 else -hanging_chars
            )
        else:
            hanging: int | str | NotFound = self._display("pPr.ind.hanging")
            if not isinstance(hanging, NotFound):
                twips = twips_measure(hanging)
                text_indent = twips if twips < 0 else -twips
        # Hanging has higher priority over firstLine elms
        if text_indent is None:
            first_line_chars: int | NotFound = self._display(
                "pPr.ind.firstLineChars"
            )
            if not isinstance(first_line_chars, NotFound):
                text_indent = first_line_chars
            else:
                first_line: int | str | NotFound = self._display(
                    "pPr.ind.firstLine"
                )
                if not isinstance(first_line, NotFound):
                    text_indent = twips_measure(first_line)
        return text_indent

    @cached_property
    def header_level(self) -> WD_HEADER_LEVEL:
        outline: int = self._display("pPr.outlineLvl.val")
        if isinstance(outline, NotFound):
            return WD_HEADER_LEVEL.TEXT
        return WD_HEADER_LEVEL(outline)

    @cached_property
    def alignment(self) -> SE_JC:
        jc = self._display("pPr.jc.val")
        if isinstance(jc, NotFound):
            return SE_JC.LEFT
        return jc

    @cached_property
    def word_wrap(self) -> bool:
        return on_off(self._display("pPr.wordWrap.val"))

    @cached_property
    def justify_inter_character(self) -> bool:
        return on_off(self._display("pPr.adjustRightInd.val"), True)

    @cached_property
    def vert_alignment(self) -> SE_TEXT_ALIGNMENT:
        v_align = self._display("pPr.textAlignment.val")
        if isinstance(v_align, NotFound):
            return SE_TEXT_ALIGNMENT.BASELINE
        return v_align

    @cached_property
    def supress_overflow(self) -> bool:
        return on_off(self._display("pPr.supressOverlap.val"))

    @cached_property
    def kinsoku(self) -> bool:
        return on_off(self._display("pPr.kinsoku.val"))

    @cached_property
    def autospace_asian_latin(self) -> bool:
        """Add space between latin-based and asian-based langs"""
        return on_off(self._display("pPr.autospaceDE.val"), True)

    @cached_property
    def autospace_asian_numbers(self) -> bool:
        return on_off(self._display("pPr.autospaceDN.val"), True)

    @cached_property
    def overflow_punct_asian(self) -> bool:
        return on_off(self._display("pPr.overflowPunct.val"))

    @cached_property
    def start_line_punct_asian(self) -> bool:
        return on_off(self._display("pPr.topLinePunct.val"))

    @cached_property
    def snap_to_grid(self) -> bool:
        return on_off(self._display("pPr.snapToGrid.val"))

    @cached_property
    def textbox_tight_wrap(self) -> bool:
        return on_off(self._display("pPr.textboxTightWrap.val"))

    @cached_property
    def mirror_indents(self) -> bool:
        """Based on the clarity of pages, determines which ind side should be reversed.

        Page number is calculated dynamically (mechanism too complex), so let’s leave it for the future,
        now consumer should determine page number.
        """
        return on_off(self._display("pPr.mirrorIndents.val", True))

    @cached_property
    def margin_top(self) -> Length | int | None:
        """Return margin on top (spacing before).

        Returns:
            Length | int | None: If `Length` - measured in twips,
                elif `int` - hundredths of a line (100 = 1 line), else auto.
        """
        if self._context_spacing:
            prev_content_item = self.prev_content_item
            if isinstance(prev_content_item, Paragraph):
                prev_style = prev_content_item.paragraph_style
                current_style = self.paragraph_style
                if (
                    prev_style is not None
                    and current_style is not None
                    and prev_style.name == current_style.name
                ):
                    return None

        if self._beforeAutospacing:
            return None
        if self._beforeLines is not None:
            return self._beforeLines
        if self._before is not None:
            return twips_measure(self._before)
        return None

    @cached_property
    def margin_bottom(self) -> Length | int | None:
        """Return margin on bottom (spacing after).

        Returns:
            Length | int | None: If `Length` - measured in twips,
                elif `int` - hundredths of a line (100 = 1 line), else auto.
        """
        if self._context_spacing:
            next_content_item = self.next_content_item
            if isinstance(next_content_item, Paragraph):
                next_style = next_content_item.paragraph_style
                current_style = self.paragraph_style
                if (
                    next_style is not None
                    and current_style is not None
                    and next_style.name == current_style.name
                ):
                    return None

        if self._afterAutospacing:
            return None
        if self._afterLines is not None:
            return self._afterLines
        if self._after is not None:
            return twips_measure(self._after)
        return None

    @cached_property
    def line_height(self) -> Length | int | None:
        """Additional spacing of paragraph block.

        For accurate interpreting this property look `line_rule` property.

        Returns:
            Length | int | None: If `Length` - measured in twips,
                elif `int` - the number represents the line spacing
                multiple of 240 (240 = 1 line), else no line height.
        """
        line: int | str | NotFound = self._display("pPr.spacing.line")
        if isinstance(line, NotFound):
            return None
        if self.line_rule == SE_LINE_SPACING_RULE.AUTO:
            if isinstance(line, str):
                return None
            return line
        return signed_twips_measure(line)

    @cached_property
    def line_rule(self) -> SE_LINE_SPACING_RULE:
        """Says how to interpret `line_height` property.

        If `AUTO`, then it's multiple of 240 (240 = 1 line),
        Else measured in twips and:
        1) When the line height is too small, the text shall be positioned at the bottom of
        the line (i.e. clipped from the top down)
        2) When the line height is too large, the text shall be centered in the available
        space.
        """
        line_rule: SE_LINE_SPACING_RULE | NotFound = self._display(
            "pPr.spacing.lineRule"
        )
        if isinstance(line_rule, NotFound):
            return SE_LINE_SPACING_RULE.AUTO
        return line_rule

    @cached_property
    def page_break_before(self) -> bool:
        return on_off(self._display("pPr.pageBreakBefore.val"))

    @cached_property
    def no_hanging(self) -> bool:
        widow_control = self._display("pPr.widowControl.val")
        if isinstance(widow_control, NotFound):
            return True
        return on_off(widow_control)

    @cached_property
    def keep_next(self) -> bool:
        return on_off(self._display("pPr.keepNext.val"))

    @cached_property
    def keep_lines(self) -> bool:
        return on_off(self._display("pPr.keepLines.val"))

    @cached_property
    def supress_line_numbers(self) -> bool:
        return on_off(self._display("pPr.suppressLineNumbers.val"))

    @cached_property
    def supress_auto_hyphens(self) -> bool:
        return on_off(self._display("pPr.suppressAutoHyphens.val"))

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
        return p_raw_text(self)

    @cached_property
    def paragraph_style(self) -> ParagraphStyle | None:
        style_id = self._prop("pPr.pStyle.val")
        if isinstance(style_id, NotFound):
            return None
        return self.document_part.styles.get_by_id(
            style_id, SE_STYLE_TYPE.PARAGRAPH, ParagraphStyle
        )

    def iter_inner_content(self) -> Iterator[PContent]:
        return p_content_iter(self)

    @cached_property
    def _context_spacing(self) -> bool:
        return on_off(self._display("pPr.contextualSpacing.val", True))

    @cached_property
    def _beforeAutospacing(self) -> bool:
        return on_off(self._display("pPr.spacing.beforeAutospacing"))

    @cached_property
    def _beforeLines(self) -> int | None:
        before = self._display("pPr.spacing.beforeLines")
        if isinstance(before, NotFound):
            return None
        return before

    @cached_property
    def _before(self) -> int | str | None:
        before = self._display("pPr.spacing.before")
        if isinstance(before, NotFound):
            return None
        return before

    @cached_property
    def _afterAutospacing(self) -> bool:
        return on_off(self._display("pPr.spacing.afterAutospacing"))

    @cached_property
    def _afterLines(self) -> int | None:
        after = self._display("pPr.spacing.afterLines")
        if isinstance(after, NotFound):
            return None
        return after

    @cached_property
    def _after(self) -> int | str | None:
        after = self._display("pPr.spacing.after")
        if isinstance(after, NotFound):
            return None
        return after

    @cached_property
    def _assoc_lvl(self) -> Level | None:
        numbering = self.document_part.numbering
        if numbering is None:
            return None
        numPr_elm = self._numPr
        if numPr_elm is None:
            num_ctx = self._para_style_num_ctx
            if num_ctx is not None:
                style, numPr_elm = num_ctx
                if numPr_elm.numId is None:
                    return None
                return numbering.associated_level(
                    numPr_elm.numId.val, style.name
                )
        else:
            if numPr_elm.numId is None:
                return None
            if numPr_elm.ilvl is None:
                return None
            return numbering.associated_level(
                numPr_elm.numId.val, numPr_elm.ilvl.val
            )
        return None

    @cached_property
    def _assoc_numPr(self) -> CT_NumPr | None:
        if self._numPr is not None:
            return self._numPr
        num_ctx = self._para_style_num_ctx
        if num_ctx is not None:
            _, numPr_elm = num_ctx
            return numPr_elm
        return None

    @cached_property
    def _para_style_num_ctx(self) -> tuple[ParagraphStyle, CT_NumPr] | None:
        if self.paragraph_style is None:
            return None
        para_style: Any = self.paragraph_style
        while isinstance(para_style, ParagraphStyle):
            numPr_elm = para_style.prop("pPr.numPr")
            if not isinstance(numPr_elm, NotFound):
                return para_style, numPr_elm
            para_style = para_style.base_style
        return None

    @cached_property
    def _rslv_order(self) -> _RslvOrder:
        if self._numPr is not None and self.paragraph_style is not None:
            return "numbering_first"
        if self._numPr is not None and self.paragraph_style is None:
            return "numbering_first"
        if self._numPr is None and self.paragraph_style is not None:
            return "paragraph_first"
        return "up_to_hierarchy"

    @cached_property
    def _numPr(self) -> CT_NumPr | None:
        numPr_elm = self._prop("pPr.numPr")
        if isinstance(numPr_elm, NotFound):
            return None
        return numPr_elm

    def _display(self, path: str, optional: bool = False) -> Any:
        # docxray stuff
        from docxray.oxml.t.proxy.table.cell import Cell

        if self.list_item:
            return self._prop(path, optional, "direct-style-hierarchy")
        para_val = self._prop(path, optional, "direct-style-hierarchy")
        if not isinstance(para_val, NotFound):
            return para_val
        if isinstance(self.container, Cell):
            tbl_val, _ = self.container._prop(path, optional, "style-ctx")
            if not isinstance(tbl_val, NotFound):
                return tbl_val
        return from_doc_dflts(self, f"pPrDefault.{path}", optional)

    def _prop_direct(self, path: str, optional: bool = False) -> Any:
        return self.prop(path, optional)

    def _prop_para_style(self, path: str, optional: bool = False) -> Any:
        if self.paragraph_style:
            return from_style_inheritance(
                self, self.paragraph_style, path, optional
            )
        return NotFound(self, path)

    def _prop_level(self, path: str, optional: bool = False) -> Any:
        if self._assoc_lvl is not None:
            num_val = self._assoc_lvl.prop(path, optional)
            if not isinstance(num_val, NotFound):
                return num_val
        return NotFound(self, path)

    def _prop_num_para_style(self, path: str, optional: bool = False) -> Any:
        p_style = None
        if self._assoc_lvl is not None:
            p_style = self._assoc_lvl.paragraph_style
        if p_style:
            style_val = from_style_inheritance(self, p_style, path, optional)
            if not isinstance(style_val, NotFound):
                return style_val
        return NotFound(self, path)

    def _prop_table_style(self, path: str, optional: bool = False) -> Any:
        # docxray stuff
        from docxray.oxml.t.proxy.table.cell import Cell

        if isinstance(self.container, Cell):
            tbl_val, _ = self.container._prop(path, optional, "style-ctx")
            if not isinstance(tbl_val, NotFound):
                return tbl_val
        return NotFound(self, path)

    def _prop_doc_dflts(self, path: str, optional: bool = False) -> Any:
        doc_val = from_doc_dflts(self, f"pPrDefault.{path}", optional)
        if not isinstance(doc_val, NotFound):
            return doc_val
        return NotFound(self, path)

    def _prop_style_hirarchy(self, path: str, optional: bool = False) -> Any:
        not_found = NotFound(self, path)
        if self._rslv_order == "numbering_first":
            search_list = [
                self._prop_level,
                self._prop_para_style,
                self._prop_num_para_style,
                self._prop_table_style,
                self._prop_doc_dflts,
            ]
        # Even if it's list item, we must follow the logic of Word renderer that
        # getting firstly property from paragraph styles in styles.xml then
        # we go to numbering
        elif self._rslv_order == "paragraph_first":
            search_list = [
                self._prop_para_style,
                self._prop_level,
                self._prop_num_para_style,
                self._prop_table_style,
                self._prop_doc_dflts,
            ]
        else:
            search_list = []
        for search_method in search_list:
            val = search_method(path, optional)
            if not isinstance(val, NotFound):
                return val
        return not_found

    def _prop(
        self,
        path: str,
        optional: bool = False,
        where: Literal[
            "direct",
            "style-hierarchy",
            "direct-style-hierarchy",
            "paragraph-style",
            "level",
            "num-paragraph-style",
            "table-style",
            "document-defaults",
        ] = "direct",
    ) -> Any:
        if where == "direct":
            return self._prop_direct(path, optional)
        elif where == "style-hierarchy":
            return self._prop_style_hirarchy(path, optional)
        elif where == "direct-style-hierarchy":
            direct_val = self._prop_direct(path, optional)
            if isinstance(direct_val, NotFound):
                return self._prop_style_hirarchy(path, optional)
            return direct_val
        elif where == "paragraph-style":
            return self._prop_para_style(path, optional)
        elif where == "level":
            return self._prop_level(path, optional)
        elif where == "table-style":
            return self._prop_table_style(path, optional)
        elif where == "document-defaults":
            return self._prop_doc_dflts(path, optional)
