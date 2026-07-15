from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from lxml.html import HtmlElement

# docxray stuff
from docxray.oxml.t.proxy.text.paragraph import PContent

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.text.list import ListItem
    from docxray.oxml.t.proxy.text.run import Run
    from docxray.transform.ruleset import RuleSet

type RunMaker = Callable[[Run | ListItem], HtmlElement | None]
type PContentFunc = Callable[
    [HtmlElement, PContent, list[RunMaker], RuleSet], None
]
