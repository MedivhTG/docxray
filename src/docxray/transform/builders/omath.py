from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

from .base import HtmlBuilder
from .std import run_omath

from docxray.oxml.trans.proxy.text.omath import (
    Accent,
    Arg,
    OMath,
    OMathParagraph,
    RunOMath,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet


class HtmlOMathPara(HtmlBuilder["OMathParagraph"]):
    @classmethod
    def element(cls, proxy: OMathParagraph, ruleset: RuleSet) -> HtmlElement:
        elm = Element("div")
        cls._fill_content(elm, proxy, ruleset)
        return elm

    @classmethod
    def _fill_content(
        cls, upper_elm: HtmlElement, proxy: OMathParagraph, ruleset: RuleSet
    ) -> None:
        for item in proxy.iter_inner_content():
            upper_elm.append(item.transform(ruleset, False))


class HtmlOMath(HtmlBuilder["OMath"]):
    WORD_TO_HTML_STRETCHY = {
        "\u0302": "\u23dc",
        "\u0303": "\u23dc",
        "\u0304": "\u23dc",
        "\u20d7": "\u2192",
        "\u20d6": "\u2190",
        "\u20e1": "\u2194",
    }

    @classmethod
    def element(cls, proxy: OMath, ruleset: RuleSet) -> HtmlElement:
        elm = Element("math")
        cls._fill_content(elm, proxy, ruleset)
        return elm

    @classmethod
    def _fill_content(
        cls, upper_elm: HtmlElement, proxy: OMath | Arg, ruleset: RuleSet
    ) -> None:
        for item in proxy.iter_inner_content():
            if isinstance(item, Accent):
                upper_elm.append(cls._accent(item, ruleset))
            elif isinstance(item, RunOMath):
                run_omath(upper_elm, item, ruleset)

    @classmethod
    def _accent(cls, accent: Accent, ruleset: RuleSet) -> HtmlElement:
        mover_elm = Element("mover", {"accent": "true"})
        chr = cls.WORD_TO_HTML_STRETCHY.get(accent.char, accent.char)
        mrow_elm = Element("mrow")
        if accent.argument:
            cls._fill_content(mrow_elm, accent.argument, ruleset)
        mover_elm.append(mrow_elm)
        mo_elm = Element("mo")
        mo_elm.text = chr
        mover_elm.append(mo_elm)
        return mover_elm
