from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

from .base import HtmlBuilder
from .html_std import (
    b_elm,
    char_elm,
    color_elm,
    i_elm,
    paragraph_content,
    strike_elm,
    underline_elm,
    vert_align_elm,
)
from .types import ElmMaker, PContentFunc

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.text.hyperlink import Hyperlink
    from docxray.transform.ruleset import RuleSet


class HtmlHyperlink(HtmlBuilder["Hyperlink"]):
    RUN_MAKERS: dict[str, ElmMaker] = {
        "vertical_alignment": vert_align_elm,
        "underline_info": underline_elm,
        "strike_case": strike_elm,
        "italic": i_elm,
        "bold": b_elm,
        "chars_case": char_elm,
        "color": color_elm,
    }
    P_CONTENT_FUNC: PContentFunc = paragraph_content

    @classmethod
    def element(cls, proxy: Hyperlink, ruleset: RuleSet) -> HtmlElement:
        elm = Element("a", cls._attrs(proxy))
        cls._fill_content(proxy, elm, ruleset)
        return elm

    @classmethod
    def _attrs(cls, proxy: Hyperlink) -> dict:
        attrs = {}
        if proxy.linked_to:
            attrs["href"] = proxy.linked_to
        if proxy.tooltip:
            attrs["title"] = proxy.tooltip
        if proxy.target_frame:
            attrs["target"] = proxy.target_frame
        return attrs

    @classmethod
    def _fill_content(
        cls, proxy: Hyperlink, elm: HtmlElement, ruleset: RuleSet
    ) -> None:
        for item in proxy.iter_inner_content():
            cls.P_CONTENT_FUNC(elm, item, cls.RUN_MAKERS, ruleset)
