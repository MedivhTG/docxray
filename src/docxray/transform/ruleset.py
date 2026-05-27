from typing import Literal, Self

from .builders import HtmlBuilder, HtmlDrawing, HtmlListView, HtmlParagraph

type RuleMethod = Literal["html"]
type RuleProxy = Literal["Paragraph", "Drawing", "ListView"]


class Rule:
    def __init__(self, builder: type[HtmlBuilder]) -> None:
        self._builder = builder

    @property
    def builder(self) -> type[HtmlBuilder]:
        return self._builder


class RuleSet:
    def __init__(self, html: dict[RuleProxy, Rule]) -> None:
        self._html = html

    @property
    def html_rules(self) -> dict[RuleProxy, Rule]:
        return self._html

    def set_html_rule(self, proxy: RuleProxy, rule: Rule | None) -> None:
        if rule is None and proxy in self._html:
            del self._html[proxy]
        if rule is not None:
            self._html[proxy] = rule

    @classmethod
    def html_default(cls) -> Self:
        return cls(
            {
                "Paragraph": Rule(HtmlParagraph),
                "Drawing": Rule(HtmlDrawing),
                "ListView": Rule(HtmlListView),
            },
        )
