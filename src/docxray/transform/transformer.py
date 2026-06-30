from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from lxml.html import HtmlElement

from ._lxml import to_str_html

type TransformMethod = Literal["html"]

if TYPE_CHECKING:
    from .ruleset import RuleProxy, RuleSet


class Transformer:
    @classmethod
    def transform(
        cls,
        proxy: Any,
        ruleset: RuleSet,
        rule_match: RuleProxy,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        if stringify:
            if method == "html":
                return cls.transform_html_stringify(proxy, ruleset, rule_match)
        if method == "html":
            return cls.transform_html(proxy, ruleset, rule_match)

    @classmethod
    def transform_html(
        cls, proxy: Any, ruleset: RuleSet, rule_match: RuleProxy
    ) -> HtmlElement:
        rule = ruleset.html_rules.get(rule_match)
        if rule is None:
            raise ValueError(
                f"No such rule for {rule_match} found in rule set"
            )
        return rule.builder.element(proxy, ruleset)

    @classmethod
    def transform_html_stringify(
        cls, proxy: Any, ruleset: RuleSet, rule_match: RuleProxy
    ) -> str:
        return to_str_html(cls.transform_html(proxy, ruleset, rule_match))
