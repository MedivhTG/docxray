from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

from .base import HtmlBuilder
from .html_std import paragraph_content

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.text.hyperlink import Hyperlink
    from docxray.oxml.t.proxy.text.paragraph import PContent
    from docxray.transform.ruleset import RuleSet


class HtmlHyperlink(HtmlBuilder["Hyperlink"]):
    P_CONTENT_FUNC: Callable[[HtmlElement, PContent, RuleSet], None] = (
        paragraph_content
    )

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
        return attrs

    @classmethod
    def _fill_content(
        cls, proxy: Hyperlink, elm: HtmlElement, ruleset: RuleSet
    ) -> None:
        for item in proxy.iter_inner_content():
            cls.P_CONTENT_FUNC(elm, item, ruleset)
