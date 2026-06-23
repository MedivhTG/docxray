from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

from .base import HtmlBuilder

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.text.omath import OMath, OMathParagraph
    from docxray.transform.ruleset import RuleSet


class HtmlOMathPara(HtmlBuilder["OMathParagraph"]):
    @classmethod
    def element(cls, proxy: OMathParagraph, ruleset: RuleSet) -> HtmlElement:
        return Element("math")


class HtmlOMath(HtmlBuilder["OMath"]):
    @classmethod
    def element(cls, proxy: OMath, ruleset: RuleSet) -> HtmlElement:
        return Element("math")
