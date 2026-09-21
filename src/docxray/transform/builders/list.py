from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

from .base import HtmlBuilder

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.text.list import (
        ListViewIlvlBlock,
        ListViewInterrupted,
    )
    from docxray.transform.ruleset import RuleSet


class HtmlListViewInterrupted(HtmlBuilder["ListViewInterrupted"]):
    @classmethod
    def element(
        cls, proxy: ListViewInterrupted, ruleset: RuleSet
    ) -> HtmlElement:
        zero_list_elm = cls._list_elm(proxy)
        cls._fill_list(zero_list_elm, proxy, ruleset)
        return zero_list_elm

    @classmethod
    def _fill_list(
        cls,
        zero_li_elm: HtmlElement,
        proxy: ListViewInterrupted,
        ruleset: RuleSet,
    ) -> None:
        ruleset_for_p = copy(ruleset)
        ruleset_for_p.set_html_rule(
            "Paragraph", ruleset.html_rules["ParagraphInList"]
        )
        for zero_block in proxy.items_tree:
            cls._process_zero_block(zero_li_elm, zero_block, ruleset_for_p)

    @classmethod
    def _process_zero_block(
        cls,
        zero_list_elm: HtmlElement,
        zero_block: ListViewIlvlBlock,
        rulset: RuleSet,
    ) -> None:
        zero_li_elm = cls._list_item_elm(zero_block)
        p_elm: HtmlElement = zero_block.li.paragraph.transform(rulset, False)
        zero_li_elm.text = p_elm.text
        zero_li_elm.extend(list(p_elm))
        zero_list_elm.append(zero_li_elm)
        if zero_block.inside_blocks:
            cls._fill_list_recursion(zero_li_elm, zero_block, rulset)

    @classmethod
    def _fill_list_recursion(
        cls,
        up_li: HtmlElement,
        block: ListViewIlvlBlock,
        ruleset_for_p: RuleSet,
    ) -> None:
        lst_elm = cls._list_elm(block)
        for block_in in block.inside_blocks:
            li_elm = cls._list_item_elm(block)
            p_elm: HtmlElement = block_in.li.paragraph.transform(
                ruleset_for_p, stringify=False
            )
            li_elm.text = p_elm.text
            li_elm.extend(list(p_elm))
            lst_elm.append(li_elm)
            if block_in.inside_blocks:
                cls._fill_list_recursion(li_elm, block_in, ruleset_for_p)
        up_li.append(lst_elm)

    @classmethod
    def _list_elm(
        cls, proxy: ListViewInterrupted | ListViewIlvlBlock
    ) -> HtmlElement:
        is_bullet = proxy.is_bullet_format
        attrs = cls._list_attrs(proxy)
        if is_bullet:
            return Element("ul", attrs)
        return Element("ol", attrs)

    @classmethod
    def _list_item_elm(cls, proxy: ListViewIlvlBlock) -> HtmlElement:
        return Element("li", cls._list_item_attrs(proxy))

    @classmethod
    def _list_attrs(
        cls, proxy: ListViewInterrupted | ListViewIlvlBlock
    ) -> dict:
        return {}

    @classmethod
    def _list_item_attrs(cls, proxy: ListViewIlvlBlock) -> dict:
        return {}
