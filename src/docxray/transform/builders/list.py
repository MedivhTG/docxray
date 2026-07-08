from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

from .base import HtmlBuilder

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.list import (
        ListViewIlvlBlock,
        ListViewInterrupted,
    )
    from docxray.transform.ruleset import RuleSet


class HtmlListViewInterrupted(HtmlBuilder["ListViewInterrupted"]):
    @classmethod
    def element(
        cls, proxy: ListViewInterrupted, ruleset: RuleSet
    ) -> HtmlElement:
        zero_lst_elm = (
            Element("ul") if proxy.is_bullet_format else Element("ol")
        )
        ruleset_for_p = copy(ruleset)
        ruleset_for_p.set_html_rule(
            "Paragraph", ruleset.html_rules["ParagraphInList"]
        )

        def fill_list(up_li: HtmlElement, block: ListViewIlvlBlock) -> None:
            bullet = block.li.is_bullet_format
            lst_elm = Element("ul") if bullet else Element("ol")
            for block_in in block.inside_blocks:
                li_elm = Element("li")
                p_elm: HtmlElement = block_in.li.paragraph.transform(
                    ruleset_for_p, stringify=False
                )
                li_elm.text = p_elm.text
                li_elm.extend(list(p_elm))

                lst_elm.append(li_elm)
                if block_in.inside_blocks:
                    fill_list(li_elm, block_in)
            up_li.append(lst_elm)

        for zero_block in proxy.items_tree:
            zero_li_elm = Element("li")
            p_elm: HtmlElement = zero_block.li.paragraph.transform(
                ruleset_for_p, False
            )
            zero_li_elm.text = p_elm.text
            zero_li_elm.extend(list(p_elm))

            zero_lst_elm.append(zero_li_elm)
            if zero_block.inside_blocks:
                fill_list(zero_li_elm, zero_block)
        return zero_lst_elm
