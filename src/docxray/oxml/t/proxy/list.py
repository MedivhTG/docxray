from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

# docxray stuff
from docxray.length import Length
from docxray.numeral.charset import DECIMAL
from docxray.numeral.numeral import Numeral
from docxray.oxml.t.proxy.numbering.numbering import Level, Numbering
from docxray.oxml.t.proxy.text.font import Font
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.proxy.text.paragraph import Paragraph
from docxray.oxml.t.proxy.text.run import CharsCase, StrikeCase, UnderlineInfo
from docxray.oxml.t.st.enums import (
    SE_HIGHLIGHT_COLOR,
    SE_NUMBER_FORMAT,
    SE_VERTICAL_ALIGN_RUN,
)
from docxray.oxml.t.text.num_props import CT_NumPr
from docxray.transform.transformer import Transformer

from .numeral_rules import (
    NUMERAL_RULES,
    NUMERAL_SPECIFIC,
    NUMERAL_WITH_LOCALE,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet
    from docxray.transform.transformer import TransformMethod

_ILVL_ALLOWED = set(DECIMAL[1:])


class ListItemError(Exception):
    pass


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

    @cached_property
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
                    prev_same_ilvl = block_map.get(item.ilvl)
                    if prev_same_ilvl is not None:
                        parent_block = prev_same_ilvl.parent
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


class ListViewInterrupted(ListView):
    def __load_items__(self, list_item: ListItem) -> None:
        next_item = list_item.paragraph.next_content_item
        items = [list_item]
        list_ends = list_item.paragraph.content_idx
        while next_item:
            if isinstance(next_item, Paragraph):
                if next_item.list_item:
                    items.append(next_item.list_item)
                    list_ends = next_item.content_idx
                else:
                    break
            else:
                break
            next_item = next_item.next_content_item
        self._items = items
        self._list_ends = list_ends

    @cached_property
    def list_ends(self) -> int:
        return self._list_ends

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        ruleset = (
            ruleset or self._li.paragraph.document_part._default_html_ruleset
        )
        return Transformer.transform(
            self, ruleset, "ListViewInterrupted", stringify, method
        )


class ListItem:
    """Represents `Paragraph` instance as list item in numbering."""

    def __init__(
        self,
        numbering: Numbering,
        paragraph: Paragraph,
        numPr_elm: CT_NumPr,
        level: Level,
    ) -> None:
        self._numbering = numbering
        self._paragraph = paragraph
        if numPr_elm.numId is None:
            raise ListItemError(
                "Cannot instantiate list item with `None` numId"
            )
        self._num_id = numPr_elm.numId.val
        self._level = level
        self._ilvl = (
            numPr_elm.ilvl.val
            if numPr_elm.ilvl is not None
            else self._level.ilvl
        )

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
        return self._ilvl

    @cached_property
    def num_key(self) -> tuple[int, int]:
        """Tuple of `num_id` and `ilvl`"""
        return self.num_id, self.ilvl

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
    def font(self) -> Font | None:
        return self.level.font

    @cached_property
    def language(self) -> Language | None:
        return self.level.language

    @cached_property
    def level_text(self) -> str:
        """Get rendered level text as in WORD."""
        level = self.level
        num_format = level.numbering_format
        if num_format in NUMERAL_SPECIFIC:
            return self._char(self)
        return self._parse_pattern(self)

    @cached_property
    def is_bullet_format(self) -> bool:
        return self.level.numbering_format == SE_NUMBER_FORMAT.BULLET

    @cached_property
    def italic(self) -> bool:
        return self.level.italic

    @cached_property
    def bold(self) -> bool:
        return self.level.bold

    @cached_property
    def chars_case(self) -> CharsCase | None:
        return self.level.chars_case

    @cached_property
    def underline_info(self) -> UnderlineInfo | None:
        return self.level.underline_info

    @cached_property
    def strike_case(self) -> StrikeCase | None:
        return self.level.strike_case

    @cached_property
    def vertical_alignment(self) -> None | SE_VERTICAL_ALIGN_RUN:
        return self.level.vertical_alignment

    @cached_property
    def color(self) -> str:
        return self.level.color

    @cached_property
    def font_size(self) -> Length | None:
        return self.level.font_size

    @cached_property
    def highlight(self) -> SE_HIGHLIGHT_COLOR | None:
        return self.level.highlight

    @cached_property
    def hide_text(self) -> bool:
        return self.level.hide_text

    def _char_ord(self, current_li: ListItem, for_ilvl: int) -> int:
        for_lvl = self._numbering.associated_level(current_li.num_id, for_ilvl)
        restart_from = for_lvl.restart_from
        prev_li: ListItem | None = current_li
        count_ilvl = 0
        while prev_li:
            if prev_li.ilvl == for_ilvl:
                count_ilvl += 1
            elif prev_li.ilvl < for_ilvl:
                # Restart every time when early levels occured
                if restart_from is None and prev_li.ilvl < for_ilvl:
                    break
                # If restart_from is 0 - never restart, else restart from mentioned level or earlier
                elif (
                    restart_from is not None
                    and restart_from != 0
                    and prev_li.ilvl < restart_from
                ):
                    break
            prev_li = prev_li.prev_li
        if count_ilvl == 0:
            count_ilvl = 1
        return for_lvl.start_from + count_ilvl - 1

    # TODO: here can be an Image instance along with common chars
    def _char(self, for_leveled: ListItem | Level, ord: int = 1) -> str:
        if isinstance(for_leveled, ListItem):
            level = for_leveled.level
        else:
            level = for_leveled
        format = level.numbering_format
        if format == SE_NUMBER_FORMAT.NONE:
            return ""
        if format == SE_NUMBER_FORMAT.BULLET:
            return level.pattern
        if format == SE_NUMBER_FORMAT.CUSTOM:
            # TODO: need hard XSLT-implementation
            return level.pattern
        if level.all_decimal:
            return Numeral.decimal(ord)
        if format in NUMERAL_WITH_LOCALE:
            locale = "en-US"
            if for_leveled.language:
                locale = for_leveled.language.latin_slot or "en-US"
            return NUMERAL_RULES[format](ord, locale)  # type: ignore[operator]
        return NUMERAL_RULES[format](ord)  # type: ignore[operator]

    def _parse_pattern(self, li: ListItem) -> str:
        text = ""
        pct_followed = False
        for ch in li.level.pattern:
            if ch == "%":
                pct_followed = True
                continue
            if not (pct_followed and ch in _ILVL_ALLOWED):
                text += ch
                continue
            ilvl_found = int(ch) - 1
            char_ord = self._char_ord(li, ilvl_found)
            text += self._char(
                self._numbering.associated_level(li.num_id, ilvl_found),
                char_ord,
            )
            pct_followed = False
        return text
