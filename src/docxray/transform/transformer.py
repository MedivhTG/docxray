from abc import abstractmethod
from typing import Any, Generic, Literal, TypeVar

from lxml.html import HtmlElement

from ._lxml import to_str_html
from .ruleset import RuleSet

type TransformMethod = Literal["html"]

T = TypeVar("T")


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
