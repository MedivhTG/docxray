from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import HtmlElement

# docxray stuff
from docxray.transform.ruleset import RuleSet

from .transformer import Transformer

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph


class ParagraphT(Transformer):
    @classmethod
    def transform_html(  # type: ignore[override]
        cls, proxy: Paragraph, ruleset: RuleSet
    ) -> HtmlElement:
        rule = ruleset.html_rules.get("Paragraph")
        if rule is None:
            raise ValueError("No such rule for Paragraph found in rule set")
        return rule.builder.element(proxy, ruleset)
