from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar

from lxml.html import HtmlElement

from ._lxml import to_str_html

type TransformMethod = Literal["html"]

T = TypeVar("T")

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph
    from docxray.oxml.trans.h2d.paragraph import ListView
    from .ruleset import RuleSet


class Transformer(Generic[T]):
    @classmethod
    def transform(
        cls,
        proxy: T,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        if method == "html":
            if stringify:
                return cls.transform_html_stringify(proxy, ruleset)
            return cls.transform_html(proxy, ruleset)
        raise ValueError(f"No such transform method {method}")

    @classmethod
    @abstractmethod
    def transform_html(
        cls, proxy: T, ruleset: RuleSet | None = None
    ) -> HtmlElement: ...

    @classmethod
    def transform_html_stringify(
        cls, proxy: T, ruleset: RuleSet | None = None
    ) -> str:
        return to_str_html(cls.transform_html(proxy, ruleset))


class ParagraphT(Transformer["Paragraph"]):
    @classmethod
    def transform_html(  # type: ignore[override]
        cls, proxy: Paragraph, ruleset: RuleSet
    ) -> HtmlElement:
        rule = ruleset.html_rules.get("Paragraph")
        if rule is None:
            raise ValueError("No such rule for Paragraph found in rule set")
        return rule.builder.element(proxy, ruleset)


class ListViewT(Transformer):
    @classmethod
    def transform_html(  # type: ignore[override]
        cls, proxy: ListView, ruleset: RuleSet
    ) -> HtmlElement:
        rule = ruleset.html_rules.get("ListView")
        if rule is None:
            raise ValueError("No such rule for Paragraph found in rule set")
        return rule.builder.element(proxy, ruleset)
