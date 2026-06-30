from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.proxy.text.omath import (
    Accent,
    Arg,
    Bar,
    BoxObject,
    OMath,
    OMathParagraph,
    RunOMath,
)
from docxray.oxml.trans.st.enums import SE_JC_OMATH, SE_TOP_BOT

from .base import HtmlBuilder
from .html_std import content_append, run_omath

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet


class HtmlOMathPara(HtmlBuilder["OMathParagraph"]):
    ALGN_MAP = {
        SE_JC_OMATH.CENTER_GROUP: "center",
        SE_JC_OMATH.LEFT: "left",
        SE_JC_OMATH.CENTER: "center",
        SE_JC_OMATH.RIGHT: "right",
    }

    @classmethod
    def element(cls, proxy: OMathParagraph, ruleset: RuleSet) -> HtmlElement:
        elm = Element("div", cls._attrs(proxy))
        cls._fill_content(elm, proxy, ruleset)
        return elm

    @classmethod
    def _attrs(cls, proxy: OMathParagraph) -> dict:
        return {"style": f"text-align: {cls.ALGN_MAP[proxy.alignment]};"}

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
        elm = Element("math", cls._attrs(proxy))
        cls._fill_content(elm, proxy, ruleset)
        return elm

    @classmethod
    def _attrs(cls, proxy: OMath) -> dict:
        attrs = {}
        if (
            isinstance(proxy._parent, OMathParagraph)
            and proxy._parent.alignment == SE_JC_OMATH.CENTER_GROUP
        ):
            attrs["style"] = "text-align: left;"
        return attrs

    @classmethod
    def _fill_content(
        cls, upper_elm: HtmlElement, proxy: OMath | Arg, ruleset: RuleSet
    ) -> None:
        for item in proxy.iter_inner_content():
            if isinstance(item, Accent):
                content_append(upper_elm, cls._accent(item, ruleset))
            elif isinstance(item, Bar):
                content_append(upper_elm, cls._bar(item, ruleset))
            elif isinstance(item, BoxObject):
                content_append(upper_elm, cls._box_object(item, ruleset))
            elif isinstance(item, RunOMath):
                run_omath(upper_elm, item, ruleset)

    @classmethod
    def _accent(cls, accent: Accent, ruleset: RuleSet) -> HtmlElement:
        mover_elm = Element("mover", {"accent": "true"})
        chr = cls.WORD_TO_HTML_STRETCHY.get(accent.char, accent.char)
        mrow_elm = Element("mrow")
        if accent.argument is not None:
            cls._fill_content(mrow_elm, accent.argument, ruleset)
        mover_elm.append(mrow_elm)
        mo_elm = Element("mo")
        mo_elm.text = chr
        mover_elm.append(mo_elm)
        return mover_elm

    # There is good analog with tag `<menclose>` but problem is.. not all browsers
    # support it (in this case - browsers with Chromium engine).
    # Info from https://developer.mozilla.org/en-US/docs/Web/MathML/Reference/Element/menclose
    @classmethod
    def _bar(cls, bar: Bar, ruleset: RuleSet) -> HtmlElement:
        decor = "overline" if bar.position == SE_TOP_BOT.TOP else "underline"
        mrow_elm = Element("mrow", {"style": f"text-decoration: {decor};"})
        if bar.argument is not None:
            cls._fill_content(mrow_elm, bar.argument, ruleset)
        return mrow_elm

    # The specification provides too little information about the attributes,
    # so we do not interpret `as_differential` (m:diff) and `as_inline_block` (m:aln)
    # and they do not have effect on text render as i saw..?
    # Plus `aln_break_at` (m:brk or Manualbreak) idk how to render with no tables (hard)
    # so we just append `br` tag and that's all (but it will break math render)
    @classmethod
    def _box_object(cls, box: BoxObject, ruleset: RuleSet) -> HtmlElement:
        attrs = {}
        if box.no_wrap:
            attrs["style"] = "white-space: nowrap;"
        mrow_elm = Element("mrow", attrs)
        if box.align_break_at:
            mrow_elm.append(Element("br"))
        if box.argument is not None:
            cls._fill_content(mrow_elm, box.argument, ruleset)
        return mrow_elm
