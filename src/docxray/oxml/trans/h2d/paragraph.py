from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.compute import (
    on_off,
    signed_twips_measure,
    twips_measure,
)
from docxray.oxml.trans.proxy.numbering.numbering import (
    Level,
    LevelOverride,
    Num,
)
from docxray.oxml.trans.proxy.shared import (
    Length,
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import (
    SE_JC,
    SE_LINE_SPACING_RULE,
    SE_TEXT_ALIGNMENT,
    SE_TEXT_DIRECTION,
    SE_StyleType,
)
from docxray.oxml.trans.text.num_props import CT_NumPr

from .how2display import How2Display
from .list_view import ListItem, ListView, ListViewInterrupted

type _DirectCase = Literal[
    "numbering_first", "paragraph_first", "up_to_hierarchy"
]
type CharsCase = Literal["up", "down"]


class ListItemError(Exception):
    pass


# TODO: Global problem [GP_1]: need text processor
# to know char positions dynmically (for tabs for example) and count pages


class ParagraphH2D(How2Display[Paragraph]):
    @cached_property
    def cell(self) -> Cell | None:
        container = self._proxy.container
        if isinstance(container, Cell):
            return container
        return None

    @cached_property
    def list_item(self) -> ListItem | None:
        if self._numbering is None:
            return None
        if self._associated_numPr is None:
            return None
        if self._associated_level is None:
            return None
        return ListItem(
            self._numbering,
            self._proxy,
            self._associated_numPr,
            self._associated_level,
        )

    @cached_property
    def list_view(self) -> ListView | None:
        if self.list_item is None:
            return None
        return ListView(self.list_item)

    @cached_property
    def list_view_interrupted(self) -> ListViewInterrupted | None:
        if self.list_item is None:
            return None
        return ListViewInterrupted(self.list_item)

    # --- Page properties
    @cached_property
    def no_hanging(self) -> bool:
        widow_control = self._display_val("widowControl")
        if isinstance(widow_control, NotFound):
            return True
        return on_off(widow_control)

    @cached_property
    def keep_next(self) -> bool:
        return on_off(self._display_val("keepNext"))

    @cached_property
    def keep_lines(self) -> bool:
        return on_off(self._display_val("keepLines"))

    @cached_property
    def page_break_before(self) -> bool:
        """Make page break before current paragraph."""
        return on_off(self._display_val("pageBreakBefore"))

    @cached_property
    def supress_line_numbers(self) -> bool:
        return on_off(self._display_val("suppressLineNumbers"))

    @cached_property
    def supress_auto_hyphens(self) -> bool:
        return on_off(self._display_val("suppressAutoHyphens"))

    # --- Page properties (end)

    # --- Indentation/interval properties
    # TODO: look GP_1
    @cached_property
    def mirror_indents(self) -> bool:
        """Based on the clarity of pages, determines which ind side should be reversed.

        Page number is calculated dynamically (mechanism too complex), so let’s leave it for the future,
        now consumer should determine page number.

        Returns:
            bool: _description_
        """
        return on_off(self._display_val("mirrorIndents"))

    @cached_property
    def right_to_left(self) -> bool:
        return on_off(self._display_val("bidi"))

    # TODO: inherit from parent Section if omitted
    @cached_property
    def text_flow(self) -> SE_TEXT_DIRECTION | None:
        val = self._display_val("textDirection")
        if not isinstance(val, NotFound):
            return val
        return None

    @cached_property
    def margin_line_start(self) -> Length | int | None:
        left_chars: int | NotFound = self._display_ind_prop("leftChars")
        if isinstance(left_chars, NotFound):
            left_chars = self._display_ind_prop("startChars")
        if isinstance(left_chars, NotFound):
            left: int | str | NotFound = self._display_ind_prop("left")
            if isinstance(left, NotFound):
                left = self._display_ind_prop("start")
            if not isinstance(left, NotFound):
                return signed_twips_measure(left)
        else:
            return left_chars
        return None

    @cached_property
    def margin_line_end(self) -> Length | int | None:
        right_chars: int | NotFound = self._display_ind_prop("rightChars")
        if isinstance(right_chars, NotFound):
            right_chars = self._display_ind_prop("endChars")
        if isinstance(right_chars, NotFound):
            right: int | str | NotFound = self._display_ind_prop("right")
            if isinstance(right, NotFound):
                right = self._display_ind_prop("end")
            if not isinstance(right, NotFound):
                return signed_twips_measure(right)
        else:
            return right_chars
        return None

    @cached_property
    def text_indent(self) -> Length | int | None:
        text_indent = None
        hanging_chars: int | NotFound = self._display_ind_prop("hangingChars")
        if not isinstance(hanging_chars, NotFound):
            text_indent = (
                hanging_chars if hanging_chars < 0 else -hanging_chars
            )
        else:
            hanging: int | str | NotFound = self._display_ind_prop("hanging")
            if not isinstance(hanging, NotFound):
                twips = twips_measure(hanging)
                text_indent = twips if twips < 0 else -twips
        # Hanging has higher priority over firstLine elms
        if text_indent is None:
            first_line_chars: int | NotFound = self._display_ind_prop(
                "firstLineChars"
            )
            if not isinstance(first_line_chars, NotFound):
                text_indent = first_line_chars
            else:
                first_line: int | str | NotFound = self._display_ind_prop(
                    "firstLine"
                )
                if not isinstance(first_line, NotFound):
                    text_indent = twips_measure(first_line)
        return text_indent

    @cached_property
    def margin_top(self) -> Length | int | None:
        """Return margin on top (spacing before).

        Returns:
            Length | int | None: If `Length` - measured in twips,
                elif `int` - hundredths of a line (100 = 1 line), else auto.
        """
        if self._context_spacing:
            prev_content_item = self._proxy.prev_content_item
            if isinstance(prev_content_item, Paragraph):
                prev_style = prev_content_item.h2d._para_style_direct
                current_style = self._para_style_direct
                if (
                    prev_style is not None
                    and current_style is not None
                    and prev_style.name == current_style.name
                ):
                    return None

        if on_off(self._display_spacing_prop("beforeAutospacing")):
            return None
        before_lines: int | NotFound = self._display_spacing_prop(
            "beforeLines"
        )
        if isinstance(before_lines, NotFound):
            before = self._display_spacing_prop("before")
            if not isinstance(before, NotFound):
                return twips_measure(before)
        else:
            return before_lines
        return None

    @cached_property
    def margin_bottom(self) -> Length | int | None:
        """Return margin on bottom (spacing after).

        Returns:
            Length | int | None: If `Length` - measured in twips,
                elif `int` - hundredths of a line (100 = 1 line), else auto.
        """
        if self._context_spacing:
            next_content_item = self._proxy.next_content_item
            if isinstance(next_content_item, Paragraph):
                next_style = next_content_item.h2d._para_style_direct
                current_style = self._para_style_direct
                if (
                    next_style is not None
                    and current_style is not None
                    and next_style.name == current_style.name
                ):
                    return None

        if on_off(self._display_spacing_prop("afterAutospacing")):
            return None
        after_lines: int | NotFound = self._display_spacing_prop("afterLines")
        if isinstance(after_lines, NotFound):
            after = self._display_spacing_prop("after")
            if not isinstance(after, NotFound):
                return twips_measure(after)
        else:
            return after_lines
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
        line: int | str | NotFound = self._display_spacing_prop("line")
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
        line_rule: SE_LINE_SPACING_RULE | NotFound = (
            self._display_spacing_prop("lineRule")
        )
        if isinstance(line_rule, NotFound):
            return SE_LINE_SPACING_RULE.AUTO
        return line_rule

    # --- Indentation/interval properties (end)

    # TODO: some properties can be deleted and used in methods after
    # --- General/specific properties

    @cached_property
    def header_level(self) -> WD_HEADER_LEVEL:
        outlineLevel_val: int = self._display_val("outlineLvl")
        if isinstance(outlineLevel_val, NotFound):
            return WD_HEADER_LEVEL.TEXT
        return WD_HEADER_LEVEL(outlineLevel_val)

    @cached_property
    def alignment(self) -> SE_JC:
        jc = self._display_val("jc")
        if isinstance(jc, NotFound):
            return SE_JC.LEFT
        return jc

    @cached_property
    def vert_alignment(self) -> SE_TEXT_ALIGNMENT:
        v_align = self._display_val("textAlignment")
        if isinstance(v_align, NotFound):
            return SE_TEXT_ALIGNMENT.BASELINE
        return v_align

    @cached_property
    def word_wrap(self) -> bool:
        return on_off(self._display_val("wordWrap"))

    @cached_property
    def justify_inter_character(self) -> bool:
        return on_off(self._display_val("adjustRightInd"), True)

    @cached_property
    def supress_overflow(self) -> bool:
        return on_off(self._display_val("supressOverlap"))

    @cached_property
    def kinsoku(self) -> bool:
        return on_off(self._display_val("kinsoku"))

    @cached_property
    def autospace_asian_latin(self) -> bool:
        """Add space between latin-based and asian-based langs"""
        return on_off(self._display_val("autospaceDE"), True)

    @cached_property
    def autospace_asian_numbers(self) -> bool:
        return on_off(self._display_val("autospaceDN"), True)

    @cached_property
    def overflow_punct_asian(self) -> bool:
        return on_off(self._display_val("overflowPunct"))

    @cached_property
    def start_line_punct_asian(self) -> bool:
        return on_off(self._display_val("topLinePunct"))

    @cached_property
    def snap_to_grid(self) -> bool:
        return on_off(self._display_val("snapToGrid"))

    @cached_property
    def textbox_tight_wrap(self) -> bool:
        return on_off(self._display_val("textboxTightWrap"))

    # --- General/specific properties (end)

    @cached_property
    def _context_spacing(self) -> bool:
        return on_off(self._display_val("contextualSpacing", True))

    @cached_property
    def _associated_level(self) -> Level | LevelOverride | None:
        numPr_elm_direct = self._numPr_para_direct

        if numPr_elm_direct is None:
            numPr_elm_style = self._numPr_para_style
            if numPr_elm_style is not None:
                para_style_num_ref = self._para_style_num_ref
                # Never
                if para_style_num_ref is None:
                    return None

                return self._case_2_num_pr_style_ref(
                    numPr_elm_style, para_style_num_ref
                )
        else:
            return self._case_1_num_pr_direct(numPr_elm_direct)
        return None

    @cached_property
    def _associated_numPr(self) -> CT_NumPr | None:
        if self._numPr_para_direct:
            return self._numPr_para_direct
        style = self._para_style_num_ref
        if style is not None:
            path = self._prop_path("numPr", self._path_base)
            numPr_elm = safe_get_prop(style.element, path)
            if not isinstance(numPr_elm, NotFound):
                return numPr_elm
        return None

    @cached_property
    def _direct_case(self) -> _DirectCase:
        if self._numPr_para_direct and self._para_style_direct:
            return "numbering_first"
        if self._numPr_para_direct and not self._para_style_direct:
            return "numbering_first"
        if not self._numPr_para_direct and self._para_style_direct:
            return "paragraph_first"
        return "up_to_hierarchy"

    @cached_property
    def _para_style_numbering(self) -> ParagraphStyle | None:
        level = self._associated_level
        if level is None:
            return None
        if isinstance(level, LevelOverride):
            if level.lvl is not None:
                return level.lvl.paragraph_style
        else:
            return level.paragraph_style
        return None

    @cached_property
    def _numPr_para_style(self) -> CT_NumPr | None:
        if self._para_style_num_ref is None:
            return None
        path = self._prop_path("numPr", self._path_base)
        numPr_elm = safe_get_prop(self._para_style_num_ref.element, path)
        if numPr_elm is None:
            return None
        return numPr_elm

    @cached_property
    def _numPr_para_direct(self) -> CT_NumPr | None:
        numPr_elm = self._prop("numPr")
        if isinstance(numPr_elm, NotFound):
            return None
        return numPr_elm

    @cached_property
    def _para_style_num_ref(self) -> ParagraphStyle | None:
        if self._para_style_direct is None:
            return None
        para_style: Any = self._para_style_direct
        path = self._prop_path("numPr", self._path_base)
        while isinstance(para_style, ParagraphStyle):
            numPr_elm = safe_get_prop(para_style.element, path)
            if not isinstance(numPr_elm, NotFound):
                return para_style
            para_style = para_style.base_style
        return None

    @cached_property
    def _para_style_direct(self) -> ParagraphStyle | None:
        style_id = self._prop_val("pStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    def _display_spacing_prop(self, name: str, optional: bool = False) -> Any:
        spacing_path = self._prop_path(name, f"{self._path_base}.spacing")
        return self._display_val(spacing_path, optional)

    def _display_ind_prop(self, name: str, optional: bool = False) -> Any:
        ind_path = self._prop_path(name, f"{self._path_base}.ind")
        return self._display_val(ind_path, optional)

    def _display_val(
        self, name_or_path: str | PropertyPath, optional: bool = False
    ) -> Any:
        if self.list_item:
            return self._prop_val(name_or_path, optional, "both")
        para_val = self._prop_val(name_or_path, optional, "both")
        if not isinstance(para_val, NotFound):
            return para_val
        cell = self.cell
        para_path = (
            name_or_path
            if isinstance(name_or_path, PropertyPath)
            else self._prop_path("val", f"{self._path_base}.{name_or_path}")
        )
        if cell:
            tbl_val, _ = self._from_tbl_style_hierarchy(
                cell.h2d._tbl_style_props_deep, para_path, optional
            )
            if not isinstance(tbl_val, NotFound):
                return tbl_val
        return self._from_doc_dflts(
            self._prop_path(para_path.join_left("pPrDefault")), optional
        )

    def _case_1_num_pr_direct(
        self, numPr_elm: CT_NumPr
    ) -> Level | LevelOverride:
        numId_elm = numPr_elm.numId
        err = InvalidXmlError(f"Wrong numbering for {numPr_elm}")
        if numId_elm is None:
            raise err
        ilvl_elm = numPr_elm.ilvl
        if ilvl_elm is None:
            raise err
        if self._numbering is None:
            raise err
        num = self._find_real_num(numId_elm.val)
        lvl = num.associated_lvl_override(ilvl_elm.val)
        if lvl is not None:
            return lvl
        return num.abstract_num.lvl_by_ilvl(ilvl_elm.val)

    def _case_2_num_pr_style_ref(
        self, numPr_elm: CT_NumPr, para_style: ParagraphStyle
    ) -> Level:
        numId_elm = numPr_elm.numId
        err = InvalidXmlError(f"Wrong numbering for {numPr_elm}")
        if numId_elm is None:
            raise err
        if self._numbering is None:
            raise err
        num = self._find_real_num(numId_elm.val)
        style_id = para_style.element.name
        if style_id is None:
            raise err
        return num.abstract_num.lvl_by_para_style(style_id.val)

    def _find_real_num(self, num_id: int) -> Num:
        if self._numbering is None:
            raise InvalidXmlError(f"Wrong numbering for {num_id}")
        num = self._numbering.get_num(num_id)
        abstract_num = num.abstract_num
        num_style = abstract_num.numbering_style
        # Real abstract num can be hidden in deep inheritance
        while num_style:
            num = num_style.num
            abstract_num = num.abstract_num
            num_style = abstract_num.numbering_style
        return num

    def _prop_val_run(self, name: str, optional: bool = True) -> Any:
        path = self._prop_path("val", f"rPr.{name}")
        return self._from_styles_hierarchy(path, optional, for_run=True)

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        for_run: bool | None = kwargs.pop("for_run", None)
        if self._direct_case == "numbering_first":
            if self._associated_level is not None and not for_run:
                numbering_val = safe_get_prop(
                    self._associated_level.element, path, optional
                )
                if not isinstance(numbering_val, NotFound):
                    return numbering_val
            if self._para_style_direct:
                style_val = self._from_style_inheritance(
                    self._para_style_direct, path, optional
                )
                if not isinstance(style_val, NotFound):
                    return style_val
            if self._para_style_numbering and not for_run:
                style_val = self._from_style_inheritance(
                    self._para_style_numbering, path, optional
                )
                if not isinstance(style_val, NotFound):
                    return style_val
        # Even if it's list item, we must follow the logic of Word renderer that
        # getting firstly property from paragraph styles in styles.xml then
        # we go to numbering
        elif self._direct_case == "paragraph_first":
            if self._para_style_direct:
                style_val = self._from_style_inheritance(
                    self._para_style_direct, path, optional
                )
                if not isinstance(style_val, NotFound):
                    return style_val
            if self._associated_level is not None and not for_run:
                numbering_val = safe_get_prop(
                    self._associated_level.element, path, optional
                )
                if not isinstance(numbering_val, NotFound):
                    return numbering_val
            if self._para_style_numbering and not for_run:
                style_val = self._from_style_inheritance(
                    self._para_style_numbering, path, optional
                )
                if not isinstance(style_val, NotFound):
                    return style_val
        return NotFound(self, path)
