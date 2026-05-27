from functools import cached_property
from typing import Literal, Self

from .builders import HtmlBuilder, HtmlDrawing, HtmlParagraph

type RuleMethod = Literal["html"]
type RuleProxy = Literal["Paragraph", "Drawing"]


class Rule:
    def __init__(self, builder: type[HtmlBuilder]) -> None:
        self._builder = builder

    @property
    def builder(self) -> type[HtmlBuilder]:
        return self._builder


class RuleSet:
    def __init__(self, html: dict[RuleProxy, Rule]) -> None:
        self._html = html

    @cached_property
    def html_rules(self) -> dict[RuleProxy, Rule]:
        return self._html

    @classmethod
    def html_default(cls) -> Self:
        return cls(
            {"Paragraph": Rule(HtmlParagraph), "Drawing": Rule(HtmlDrawing)}
        )
