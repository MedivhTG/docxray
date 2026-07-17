from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.t.proxy.text.omath import OMath, OMathParagraph
from docxray.oxml.t.st.enums import SE_JC_OMATH

from .base import HtmlBuilder
from .html_std import omath_to_mathjax

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
        elm = Element("span", cls._attrs(proxy))
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

    # TODO: without run style
    @classmethod
    def element(cls, proxy: OMath, ruleset: RuleSet) -> HtmlElement:
        mathjax = omath_to_mathjax(proxy)
        if mathjax:
            span_elm = Element("span", cls._attrs(proxy))
            span_elm.append(cls._script())
            p_elm = Element("p")
            # MathJax must understand LaTeX
            p_elm.text = mathjax
            span_elm.append(p_elm)
            return span_elm
        else:
            return Element("p", cls._attrs(proxy))

    @classmethod
    def _script(cls) -> HtmlElement:
        return Element(
            "script",
            {
                "src": "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
            },
        )

    @classmethod
    def _attrs(cls, proxy: OMath) -> dict:
        attrs = {}
        if (
            isinstance(proxy._parent, OMathParagraph)
            and proxy._parent.alignment == SE_JC_OMATH.CENTER_GROUP
        ):
            attrs["style"] = "text-align: left;"
        return attrs
