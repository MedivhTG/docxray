from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from lxml.html import HtmlElement

# docxray stuff
from docxray.oxml.t.proxy.text.paragraph import PContent

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet

type ElmMaker = Callable[[Any], HtmlElement]
type PContentFunc = Callable[
    [HtmlElement, PContent, dict[str, ElmMaker], RuleSet], None
]
