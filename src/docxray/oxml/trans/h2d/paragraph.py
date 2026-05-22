from functools import cached_property
from typing import Any, Literal

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.numeral.charset import DECIMAL
from docxray.numeral.numeral import Numeral
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
    SE_LEVEL_SUFFIX,
    SE_NUMBER_FORMAT,
    SE_TEXT_ALIGNMENT,
    SE_StyleType,
)
from docxray.oxml.trans.text.num_props import CT_NumPr
from docxray.shared import os_locale

from .how2display import How2Display
from .numeral_rules import NUMERAL_RULES, NUMERAL_SPECIFIC, NUMERAL_WITH_LOCALE

type Direction = Literal["rtl", "ltr"]
type _DirectCase = Literal[
    "numbering_first", "paragraph_first", "up_to_hierarchy"
]
_ILVL_ALLOWED = set(DECIMAL[1:])


# TODO: need to think about numbering refac
class ParagraphH2D(How2Display[Paragraph]):
    @cached_property
    def cell(self) -> Cell | None:
        container = self._proxy.container
        if isinstance(container, Cell):
            return container
        return None

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
    def direction(self) -> Direction:
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
    def header_level(self) -> WD_HEADER_LEVEL:
        outlineLevel_val: int = self._display_val("outlineLvl", False)
        if isinstance(outlineLevel_val, NotFound):
            return WD_HEADER_LEVEL.TEXT
        return WD_HEADER_LEVEL(outlineLevel_val)

    @cached_property
    def alignment(self) -> SE_JC:
        jc = self._display_val("jc", False)
        if isinstance(jc, NotFound):
            return SE_JC.LEFT
        return jc

    @cached_property
    def vert_alignment(self) -> SE_TEXT_ALIGNMENT:
        v_align = self._display_val("textAlignment", False)
        if isinstance(v_align, NotFound):
            return SE_TEXT_ALIGNMENT.BASELINE
        return v_align

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
    def _num_ord(self) -> int | None:
        if not self._is_list_item:
            return None
        prev_num_para = self._prev_num_para_full_search
        count = 1
        while prev_num_para:
            count += 1
            prev_num_para = prev_num_para.h2d._prev_num_para_full_search
        return count

    @cached_property
    def _next_num_para_full_search(self) -> Paragraph | None:
        if self._num_id_ilvl is None:
            return None
        next_para: Paragraph | None = self._proxy.next_sibling
        num_id, _ = self._num_id_ilvl
        while next_para:
            if self._num_id_ilvl == next_para.h2d._num_id_ilvl:
                return next_para
            next_num_id_ilvl = next_para.h2d._num_id_ilvl
            if next_num_id_ilvl is None:
                next_para = next_para.next_sibling
                continue
            num_id_next, _ = next_num_id_ilvl
            if num_id == num_id_next:
                return next_para
            next_para = next_para.next_sibling
        return None

    @cached_property
    def _prev_num_para_full_search(self) -> Paragraph | None:
        if self._num_id_ilvl is None:
            return None
        next_para: Paragraph | None = self._proxy.prev_sibling
        num_id, _ = self._num_id_ilvl
        while next_para:
            if self._num_id_ilvl == next_para.h2d._num_id_ilvl:
                return next_para
            next_num_id_ilvl = next_para.h2d._num_id_ilvl
            if next_num_id_ilvl is None:
                next_para = next_para.prev_sibling
                continue
            num_id_next, _ = next_num_id_ilvl
            if num_id == num_id_next:
                return next_para
            next_para = next_para.prev_sibling
        return None

    @cached_property
    def _num_ilvl_ord(self) -> int | None:
        if not self._is_list_item:
            return None
        prev_num_para = self._prev_num_para
        count = 1
        while prev_num_para:
            count += 1
            prev_num_para = prev_num_para.h2d._prev_num_para
        return count

    @cached_property
    def _next_num_para(self) -> Paragraph | None:
        if self._num_id_ilvl is None:
            return None
        next_para: Paragraph | None = self._proxy.next_sibling
        while next_para:
            if self._num_id_ilvl == next_para.h2d._num_id_ilvl:
                return next_para
            next_para = next_para.next_sibling
        return None

    @cached_property
    def _prev_num_para(self) -> Paragraph | None:
        if self._num_id_ilvl is None:
            return None
        next_para: Paragraph | None = self._proxy.prev_sibling
        while next_para:
            if self._num_id_ilvl == next_para.h2d._num_id_ilvl:
                return next_para
            next_para = next_para.prev_sibling
        return None

    @cached_property
    def _num_id_ilvl(self) -> tuple[int, int] | None:
        err = InvalidXmlError("Cannot determine associated numbering")
        numPr_elm = self._associated_numPr
        if numPr_elm is None:
            return None
        if numPr_elm.numId is None:
            raise err
        num_id = numPr_elm.numId.val
        if numPr_elm.ilvl is not None:
            ilvl = numPr_elm.ilvl.val
        else:
            level = self._associated_level
            if level is None:
                raise err
            if isinstance(level, LevelOverride):
                if level.lvl is None:
                    raise err
                ilvl = level.lvl.ilvl
            else:
                ilvl = level.ilvl
        return num_id, ilvl

    @cached_property
    def _is_list_item(self) -> bool:
        return self._associated_level is not None

    @cached_property
    def _associated_level_definition(self) -> Level | None:
        if self._associated_level is None:
            return None
        if self._num_id_ilvl is None:
            return None
        level = self._associated_level
        num_id, ilvl = self._num_id_ilvl
        if isinstance(level, LevelOverride):
            if level.lvl is None:
                if self._numbering is None:
                    return None
                return self._numbering.associated_lvl(num_id, ilvl)
            return level.lvl
        return level

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

    # TODO: implement (for _level_char too):
    # 1) Realize numerals
    @cached_property
    def _level_text(self) -> str | None:
        num_id_ilvl = self._num_id_ilvl
        if num_id_ilvl is None:
            return None
        _, ilvl = num_id_ilvl
        lvl = self._associated_level_definition
        if lvl is None:
            return None
        numFmt_elm = lvl.element.numFmt
        if numFmt_elm is None:
            return None
        if numFmt_elm.val in NUMERAL_SPECIFIC:
            return self._level_char
        lvlText_elm = lvl.element.lvlText
        if lvlText_elm is None:
            return None
        pattern = lvlText_elm.val
        if pattern is None:
            return None
        text = self._parse_num_pattern(pattern, ilvl)
        if lvl.separator == SE_LEVEL_SUFFIX.TAB:
            # TODO: it's not a tab as in WORD, but reproducing tab width.. is challenge
            text += "\t"
        elif lvl.separator == SE_LEVEL_SUFFIX.SPACE:
            text += " "
        return text

    @cached_property
    def _num_locale(self) -> str | None:
        lvl = self._associated_level_definition
        if lvl is None:
            return None
        if lvl.locale is not None:
            return lvl.locale
        if self._styles.document_defaults is not None:
            locale = self._styles.document_defaults.locale
            if locale is not None:
                return locale
        return os_locale()

    # TODO: here can be an Image instance along with common chars -
    # implement after
    @cached_property
    def _level_char(self) -> str | None:
        # Simple check for None values
        if self._num_id_ilvl is None:
            return None
        num_id, ilvl = self._num_id_ilvl
        if self._num_ilvl_ord is None:
            return None
        if self._associated_level is None:
            return None

        # Get start and level
        level = self._associated_level
        start = 0
        if isinstance(level, LevelOverride):
            if level.lvl is None:
                if self._numbering is None:
                    return None
                lvl = self._numbering.associated_lvl(num_id, ilvl)
            else:
                lvl = level.lvl
            startOverride = level.element.startOverride
            if startOverride is not None:
                start = startOverride.val
            elif lvl.element.start is not None:
                start = lvl.element.start.val
        else:
            lvl = level
            if lvl.element.start is not None:
                start = lvl.element.start.val

        # Numbering format
        numFmt_elm = lvl.element.numFmt
        if numFmt_elm is None:
            return None
        if numFmt_elm.val == SE_NUMBER_FORMAT.NONE:
            return None

        # Get right ord
        if ilvl == 0:
            # Never restarts (highest level)
            ord = self._num_ilvl_ord + start - 1
        else:
            if lvl.element.lvlRestart is None:
                restart_lvl = None
                upper_lvl = ilvl - 1
            else:
                restart_lvl = lvl.element.lvlRestart.val
                upper_lvl = ilvl - restart_lvl

            if restart_lvl == 0:
                # Never restarts (restart level is 0)
                ord = self._num_ilvl_ord + start - 1
            else:
                restart = False
                same_level_count = 1
                prev_para = self._prev_num_para_full_search
                while prev_para:
                    prev_num_id_ilvl = prev_para.h2d._num_id_ilvl
                    if prev_num_id_ilvl is None:
                        prev_para = prev_para.h2d._prev_num_para_full_search
                        continue
                    _, prev_ilvl = prev_num_id_ilvl
                    if prev_ilvl == ilvl:
                        same_level_count += 1
                    if prev_ilvl <= upper_lvl:
                        restart = True
                        break
                    prev_para = prev_para.h2d._prev_num_para_full_search
                if restart:
                    # Restart with count of the same level found before
                    ord = same_level_count + start - 1
                else:
                    # Not restarts (not found higher level)
                    ord = self._num_ilvl_ord + start - 1

        if numFmt_elm.val == SE_NUMBER_FORMAT.BULLET:
            # TODO: plug for a while (or not)
            return Numeral.bullet(ilvl)
        if numFmt_elm.val == SE_NUMBER_FORMAT.CUSTOM:
            if numFmt_elm.format is None:
                return None
            return Numeral.custom(ord, numFmt_elm.format)
        to_decimal = (
            on_off(lvl.element.isLgl)
            if lvl.element.isLgl is not None
            else False
        )
        if to_decimal:
            return Numeral.decimal(ord)
        if numFmt_elm.val in NUMERAL_WITH_LOCALE:
            locale = self._num_locale or "en-US"
            return NUMERAL_RULES[numFmt_elm.val](ord, locale)  # type: ignore[operator]
        return NUMERAL_RULES[numFmt_elm.val](ord)  # type: ignore[operator]

    def _parse_num_pattern(self, pattern: str, ilvl: int) -> str:
        text = ""
        percentage_followed = False
        for ch in pattern:
            if ch == "%":
                percentage_followed = True
                continue
            if percentage_followed and ch in _ILVL_ALLOWED:
                ilvl_found = int(ch) - 1
                if ilvl_found == ilvl:
                    if self._level_char is not None:
                        text += self._level_char
                if ilvl_found < ilvl:
                    prev_para = self._prev_num_para_full_search
                    while prev_para:
                        prev_num_id_ilvl = prev_para.h2d._num_id_ilvl
                        if prev_num_id_ilvl is None:
                            prev_para = (
                                prev_para.h2d._prev_num_para_full_search
                            )
                            # Never
                            break
                        _, prev_ilvl = prev_num_id_ilvl
                        if prev_ilvl == ilvl_found:
                            found_lvl_ch = prev_para.h2d._level_char
                            if found_lvl_ch is not None:
                                text += found_lvl_ch
                                break
                        prev_para = prev_para.h2d._prev_num_para_full_search
                # If more than current -> ignore
            else:
                text += ch
            percentage_followed = False
        return text

    def _display_ind_prop(self, name: str, optional: bool = False) -> Any:
        para_path = self._prop_path(name, f"{self._path_base}.ind")
        return self._display_val(para_path, optional)

    def _display_val(
        self, name_or_path: str | PropertyPath, optional: bool = True
    ) -> Any:
        if self._is_list_item:
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
