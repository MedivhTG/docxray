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
from docxray.oxml.trans.st.enums import SE_StyleType
from docxray.oxml.trans.text.num_props import CT_NumPr

from .how2display import How2Display

type _Dir = Literal["rtl", "ltr"]
type _DirectCase = Literal[
    "numbering_first", "paragraph_first", "up_to_hierarchy"
]


class ParagraphH2D(How2Display[Paragraph]):
    @cached_property
    def cell(self) -> Cell | None:
        container = self._proxy.container
        if isinstance(container, Cell):
            return container
        return None

    @cached_property
    def is_list_item(self) -> bool:
        return self._associated_level is not None

    @cached_property
    def header_level(self) -> WD_HEADER_LEVEL:
        outlineLevel_val: int = self._display_val("outlineLvl", False)
        if isinstance(outlineLevel_val, NotFound):
            return WD_HEADER_LEVEL.TEXT
        return WD_HEADER_LEVEL(outlineLevel_val)

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
        return on_off(self._display_val("pageBreakBefore"))

    @cached_property
    def supress_line_numbers(self) -> bool:
        return on_off(self._display_val("suppressLineNumbers"))

    @cached_property
    def supress_auto_hyphens(self) -> bool:
        return on_off(self._display_val("suppressAutoHyphens"))

    # --- Page properties (end)

    # --- Indentation/interval properties
    # TODO: if no need -> use only in indentation property and delete it
    @cached_property
    def mirror_indents(self) -> bool:
        return on_off(self._display_val("mirrorIndents"))

    @cached_property
    def context_spacing(self) -> bool:
        return on_off(self._display_val("contextualSpacing"))

    # TODO: look for textDirection too
    @cached_property
    def direction(self) -> _Dir:
        val = on_off(self._display_val("bidi"))
        return "rtl" if val is True else "ltr"

    # TODO: add fallback on `start` and `startChars` properties
    @cached_property
    def margin_line_start(self) -> Length | int | None:
        margin_inline_start = None
        left_chars: int | NotFound = self._display_ind_prop("leftChars")
        if not isinstance(left_chars, NotFound):
            margin_inline_start = left_chars
        else:
            left: int | str | NotFound = self._display_ind_prop("left", False)
            if not isinstance(left, NotFound):
                margin_inline_start = signed_twips_measure(left)
        return margin_inline_start

    # TODO: add fallback on `end` and `endChars` properties
    @cached_property
    def margin_line_end(self) -> Length | int | None:
        margin_inline_end = None
        right_chars: int | NotFound = self._display_ind_prop("rightChars")
        if not isinstance(right_chars, NotFound):
            margin_inline_end = right_chars
        else:
            right: int | str | NotFound = self._display_ind_prop(
                "right", False
            )
            if not isinstance(right, NotFound):
                margin_inline_end = signed_twips_measure(right)
        return margin_inline_end

    @cached_property
    def text_indent(self) -> Length | int | None:
        text_indent = None
        hanging_chars: int | NotFound = self._display_ind_prop("hangingChars")
        if not isinstance(hanging_chars, NotFound):
            text_indent = (
                hanging_chars if hanging_chars < 0 else -hanging_chars
            )
        else:
            hanging: int | str | NotFound = self._display_ind_prop(
                "hanging", False
            )
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
                    "firstLine", False
                )
                if not isinstance(first_line, NotFound):
                    text_indent = twips_measure(first_line)
        return text_indent

    # --- Indentation/interval properties (end)

    # TODO: some properties can be deleted and used in methods after
    # --- General/specific properties

    @cached_property
    def word_wrap(self) -> bool:
        return on_off(self._display_val("wordWrap"))

    @cached_property
    def justify_inter_character(self) -> bool:
        return on_off(self._display_val("adjustRightInd"))

    @cached_property
    def supress_overflow(self) -> bool:
        return on_off(self._display_val("supressOverlap"))

    @cached_property
    def kinsoku(self) -> bool:
        return on_off(self._display_val("kinsoku"))

    @cached_property
    def autospace_asian_latin(self) -> bool:
        return on_off(self._display_val("autospaceDE"))

    @cached_property
    def autospace_asian_numbers(self) -> bool:
        return on_off(self._display_val("autospaceDN"))

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

    def _display_ind_prop(self, name: str, optional: bool = False) -> Any:
        para_path = self._prop_path(name, f"{self._path_base}.ind")
        return self._display_val(para_path, optional)

    def _display_val(
        self, name_or_path: str | PropertyPath, optional: bool = True
    ) -> Any:
        if self.is_list_item:
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
