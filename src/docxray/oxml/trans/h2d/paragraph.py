from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, cast

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.numeral.charset import DECIMAL
from docxray.numeral.numeral import Numeral
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.h2d.exceptions import DisplayError
from docxray.oxml.trans.proxy.compute import (
    on_off,
    signed_twips_measure,
    twips_measure,
)
from docxray.oxml.trans.proxy.numbering.numbering import (
    Level,
    LevelOverride,
    Num,
    Numbering,
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
from docxray.oxml.trans.proxy.table import Cell, Table
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import (
    SE_JC,
    SE_LINE_SPACING_RULE,
    SE_NUMBER_FORMAT,
    SE_TEXT_ALIGNMENT,
    SE_TEXT_DIRECTION,
    SE_StyleType,
    SE_Underline,
    SE_VerticalAlignRun,
)
from docxray.oxml.trans.text.num_props import CT_NumPr
from docxray.shared import os_locale

from .how2display import How2Display
from .numeral_rules import NUMERAL_RULES, NUMERAL_SPECIFIC, NUMERAL_WITH_LOCALE

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet
    from docxray.transform.transformers import TransformMethod

type _DirectCase = Literal[
    "numbering_first", "paragraph_first", "up_to_hierarchy"
]
type CharsCase = Literal["up", "down"]
_ILVL_ALLOWED = set(DECIMAL[1:])


class ListItemError(Exception):
    pass


# TODO: Global problem [GP_1]: need text processor
# to know char positions dynmically (for tabs for example) and count pages


class ListViewIlvlBlock:
    def __init__(self, li: ListItem, parent: ListViewIlvlBlock | None) -> None:
        self._li = li
        self._parent = parent
        self._block: list[ListViewIlvlBlock] = []

    @cached_property
    def li(self) -> ListItem:
        return self._li

    @cached_property
    def ilvl(self) -> int:
        return self._li.ilvl

    @cached_property
    def parent(self) -> ListViewIlvlBlock | None:
        return self._parent

    @cached_property
    def inside_blocks(self) -> list[ListViewIlvlBlock]:
        return self._block

    def append(self, block: ListViewIlvlBlock) -> None:
        if block.ilvl <= self.ilvl:
            raise ValueError(
                "Cannot append block with ilvl less or equal to parent"
            )
        self._block.append(block)


class ListView:
    def __init__(self, list_item: ListItem) -> None:
        self._li = list_item
        self.__load_items__(list_item)

    def __load_items__(self, list_item: ListItem) -> None:
        first_item = list_item
        prev_li = first_item.prev_li
        while prev_li:
            first_item = prev_li
            prev_li = prev_li.prev_li
        items = [first_item]
        next_li = first_item.next_li
        while next_li:
            items.append(next_li)
            next_li = next_li.next_li
        self._items = items

    @property
    def items(self) -> list[ListItem]:
        return self._items

    @cached_property
    def items_tree(self) -> list[ListViewIlvlBlock]:
        zero_blocks = []
        block_map: dict[int, ListViewIlvlBlock] = {}
        prev_ilvl = None
        for item in self.items:
            block = ListViewIlvlBlock(item, None)
            if prev_ilvl is not None:
                if prev_ilvl < item.ilvl:
                    block._parent = block_map[prev_ilvl]
                    block_map[prev_ilvl].append(block)
                elif prev_ilvl > item.ilvl:
                    parent_block = block_map[item.ilvl].parent
                    block._parent = parent_block
                    if parent_block is not None:
                        parent_block.append(block)
                    on_del = set()
                    for ilvl in block_map.keys():
                        if ilvl >= item.ilvl:
                            on_del.add(ilvl)
                    for ilvl in on_del:
                        del block_map[ilvl]
                else:
                    parent_block = block_map[item.ilvl].parent
                    block._parent = parent_block
                    if parent_block is not None:
                        parent_block.append(block)
            block_map[item.ilvl] = block
            if block.parent is None:
                zero_blocks.append(block)
            prev_ilvl = item.ilvl
        return zero_blocks

    @cached_property
    def is_bullet_format(self) -> bool:
        return self._li.is_bullet_format

    @cached_property
    def keeps_lists_inside(self) -> set[int]:
        all_lists = set()
        for item in self.items:
            all_lists |= item.keeps_lists_inside
        return all_lists

    @cached_property
    def keeps_commons_inside(self) -> set[int]:
        all_commons = set()
        for item in self.items:
            all_commons |= item.keeps_commons_inside
        return all_commons

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart
        from docxray.transform.transformers import ListViewT

        ruleset = (
            ruleset
            or cast(
                "DocumentPart", self._li._paragraph.part
            )._default_html_ruleset
        )
        return ListViewT.transform(self, ruleset, stringify, method)


class ListItem:
    """Represents `Paragraph` instance as list item in numbering."""

    def __init__(
        self,
        numbering: Numbering,
        paragraph: Paragraph,
        numPr_elm: CT_NumPr,
        level: Level | LevelOverride,
    ) -> None:
        self._numbering = numbering
        self._paragraph = paragraph
        self._h2d = paragraph.h2d
        if numPr_elm.numId is None:
            raise ListItemError(
                "Cannot instantiate list item with `None` numId"
            )
        self._num_id = numPr_elm.numId.val
        self._ilvl = numPr_elm.ilvl.val if numPr_elm.ilvl is not None else None
        self._start = None
        if isinstance(level, LevelOverride):
            if level.lvl is None:
                if self._ilvl is None:
                    raise ListItemError(
                        "Cannot instantiate list item wit `None` ilvl for LevelOverride"
                    )
                self._level = self._numbering.associated_lvl(
                    self._num_id, self._ilvl
                )
            else:
                self._level = level.lvl
            self._start = level.start_from
        else:
            self._level = level
            self._start = level.start_from
        if self._ilvl is None:
            self._ilvl = self._level.ilvl
        if self._start is None:
            self._start = 0

    @cached_property
    def paragraph(self) -> Paragraph:
        return self._paragraph

    @cached_property
    def level(self) -> Level:
        """Associated level with properties for list."""
        return self._level

    @cached_property
    def num_id(self) -> int:
        """Reference to numbering properties."""
        return self._num_id

    @cached_property
    def ilvl(self) -> int:
        """Hierarchy level of list item."""
        return cast("int", self._ilvl)

    @cached_property
    def num_key(self) -> tuple[int, int]:
        """Tuple of `num_id` and `ilvl`"""
        return self.num_id, self.ilvl

    @cached_property
    def start(self) -> int:
        """Which number of ordinal (or 0) must be the start of list for `char_ord`."""
        return cast("int", self._start)

    @cached_property
    def ord(self) -> int:
        """Ordinal number of list item at all."""
        prev_li = self.prev_li
        count = 1
        while prev_li:
            count += 1
            prev_li = prev_li.prev_li
        return count

    @cached_property
    def ilvl_ord(self) -> int:
        """Ordinal number of list item with the same hierarchy level (`ilvl`)."""
        prev_li = self.prev_li_ilvl
        count = 1
        while prev_li:
            count += 1
            prev_li = prev_li.prev_li_ilvl
        return count

    @cached_property
    def char_ord(self) -> int:
        """Ordinal number of character in associated charset from `Numeral` module."""
        if self.ilvl == 0:
            # Never restarts (highest level)
            return self.ilvl_ord + self.start - 1
        if self.level.restart_from is None:
            restart_lvl = None
            upper_lvl = self.ilvl - 1
        else:
            restart_lvl = self.level.restart_from
            upper_lvl = self.ilvl - restart_lvl

        if restart_lvl == 0:
            # Never restarts (restart level is 0)
            return self.ilvl_ord + self.start - 1
        restarting = False
        same_level_count = 1
        prev_li = self.prev_li
        while prev_li:
            if prev_li.ilvl == self.ilvl:
                same_level_count += 1
            if prev_li.ilvl <= upper_lvl:
                restarting = True
                break
            prev_li = prev_li.prev_li
        if restarting:
            # Restart with count of the same level found before
            return same_level_count + self.start - 1
        # Not restarts (not found higher level)
        return self.ilvl_ord + self.start - 1

    @cached_property
    def next_li(self) -> ListItem | None:
        """Next list item in all list. `None` if no list item ahead."""
        next_para: Paragraph | None = self._paragraph.next_para
        while next_para:
            if next_para.list_item is not None:
                next_li = next_para.list_item
                if self.num_key == next_li.num_key:
                    return next_li
                if self.num_id == next_li.num_id:
                    return next_li
            next_para = next_para.next_para
        return None

    @cached_property
    def prev_li(self) -> ListItem | None:
        """Previous list item in all list. `None` if no list item behind."""
        prev_para: Paragraph | None = self._paragraph.prev_para
        while prev_para:
            if prev_para.list_item is not None:
                prev_li = prev_para.list_item
                if self.num_key == prev_li.num_key:
                    return prev_li
                if self.num_id == prev_li.num_id:
                    return prev_li
            prev_para = prev_para.prev_para
        return None

    @cached_property
    def next_li_ilvl(self) -> ListItem | None:
        """Next list item in with same `ilvl`. `None` if no list item ahead."""
        next_para: Paragraph | None = self._paragraph.next_para
        while next_para:
            if next_para.list_item is not None:
                next_li = next_para.list_item
                if self.num_key == next_li.num_key:
                    return next_li
            next_para = next_para.next_para
        return None

    @cached_property
    def prev_li_ilvl(self) -> ListItem | None:
        """Previous list item in with same `ilvl`. `None` if no list item behind."""
        prev_para: Paragraph | None = self._paragraph.prev_para
        while prev_para:
            if prev_para.list_item is not None:
                prev_li = prev_para.list_item
                if self.num_key == prev_li.num_key:
                    return prev_li
            prev_para = prev_para.prev_para
        return None

    @cached_property
    def locale(self) -> str:
        """Locale set for `Numeral` module.

        Can determine which alphabet/spellout letters/numbering will be used in `level_text`.
        """
        if self.level.locale is not None:
            return self.level.locale
        if self._h2d._styles.document_defaults is not None:
            locale = self._h2d._styles.document_defaults.locale
            if locale is not None:
                return locale
        return os_locale()

    @cached_property
    def level_text(self) -> str:
        """Get rendered level text as in WORD.

        `NOTE`:
        1) For future level text can return `Image` instance (str | Image) if numbering
        format has picture reference (bullet format usually).
        """
        level = self.level
        num_format = level.numbering_format
        if num_format in NUMERAL_SPECIFIC:
            return self._level_char
        return self._parse_pattern()

    @cached_property
    def is_bullet_format(self) -> bool:
        return self.level.numbering_format == SE_NUMBER_FORMAT.BULLET

    @cached_property
    def keeps_lists_inside(self) -> set[int]:
        def inside(
            item: ListItem,
        ) -> set[int]:
            if item.next_li is None:
                return set()
            next_item = item.paragraph.next_content_item
            list_ids = set()
            while next_item:
                if isinstance(next_item, Paragraph):
                    if (
                        next_item.list_view
                        and next_item.list_view._li.num_id != item.num_id
                    ):
                        list_ids.add(next_item.list_view._li.num_id)
                next_item = next_item.next_content_item
            return list_ids

        return inside(self)

    @cached_property
    def keeps_commons_inside(self) -> set[int]:
        def inside(
            item: ListItem,
        ) -> set[int]:
            if item.next_li is None:
                return set()
            next_item = item.paragraph.next_content_item
            content_ids = set()
            while next_item:
                if isinstance(next_item, Table):
                    content_ids.add(next_item.content_idx)
                elif not next_item.list_view:
                    content_ids.add(next_item.content_idx)
                elif next_item.list_view._li.num_id == item.num_id:
                    if next_item.list_view._li.next_li is None:
                        break
                next_item = next_item.next_content_item
            return content_ids

        return inside(self)

    @cached_property
    def italic(self) -> bool:
        return self._display_level_text_run_val_on_off("i")

    @cached_property
    def bold(self) -> bool:
        return self._display_level_text_run_val_on_off("b")

    @cached_property
    def chars_case(self) -> CharsCase | None:
        if self._all_uppercase and self._all_downcase:
            raise DisplayError(
                "Mentiond 2 cases (up, down) when they are mutually exclusive"
            )
        if self._all_uppercase:
            return "up"
        if self._all_downcase:
            return "down"
        return None

    @cached_property
    def underline(self) -> None | SE_Underline:
        line = self._display_level_text_run_val("u", True)
        if isinstance(line, NotFound) or line == SE_Underline.NONE:
            return None
        if line is None:
            return SE_Underline.SINGLE
        return line

    @cached_property
    def strike(self) -> bool:
        return self._display_level_text_run_val_on_off("strike")

    @cached_property
    def vertical_alignment(self) -> None | SE_VerticalAlignRun:
        align = self._display_level_text_run_val("vertAlign")
        if (
            isinstance(align, NotFound)
            or align == SE_VerticalAlignRun.BASELINE
        ):
            return None
        return align

    @cached_property
    def _all_uppercase(self) -> bool:
        return self._display_level_text_run_val_on_off("caps")

    @cached_property
    def _all_downcase(self) -> bool:
        return self._display_level_text_run_val_on_off("smallCaps")

    # TODO: here can be an Image instance along with common chars
    @cached_property
    def _level_char(self) -> str:
        format = self.level.numbering_format
        if format == SE_NUMBER_FORMAT.NONE:
            return ""
        if format == SE_NUMBER_FORMAT.BULLET:
            if self.level.font is None:
                font = "Symbol"
            else:
                font = self.level.font.font_name
            return Numeral.bullet(self.level.pattern, font)
        if format == SE_NUMBER_FORMAT.CUSTOM:
            return Numeral.custom(
                self.char_ord, self.level.numbering_custom_pattern
            )
        if self.level.all_decimal:
            return Numeral.decimal(self.char_ord)
        if format in NUMERAL_WITH_LOCALE:
            locale = self.locale or "en-US"
            return NUMERAL_RULES[format](self.char_ord, locale)  # type: ignore[operator]
        return NUMERAL_RULES[format](self.char_ord)  # type: ignore[operator]

    def _display_level_text_run_val(
        self, name: str, optional: bool = False
    ) -> Any:
        path = PropertyPath.base("val", f"rPr.{name}")
        return self.paragraph.h2d._prop(path, optional, "style")

    def _display_level_text_run_val_on_off(self, name: str) -> bool:
        return on_off(self._display_level_text_run_val(name, True))

    def _parse_pattern(self) -> str:
        text = ""
        percentage_followed = False
        for ch in self.level.pattern:
            if ch == "%":
                percentage_followed = True
                continue
            if not (percentage_followed and ch in _ILVL_ALLOWED):
                text += ch
                continue
            ilvl_found = int(ch) - 1
            if ilvl_found == self.ilvl:
                text += self._level_char
            elif ilvl_found < self.ilvl:
                prev_li = self.prev_li
                while prev_li:
                    if prev_li.ilvl == ilvl_found:
                        text += prev_li._level_char
                        break
                    prev_li = prev_li.prev_li
            percentage_followed = False
        return text


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
        if isinstance(val, NotFound):
            return None
        return val

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
