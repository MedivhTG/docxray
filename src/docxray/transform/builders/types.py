from collections.abc import Callable
from typing import Any

from lxml.html import HtmlElement

type ElmMaker = Callable[[Any], HtmlElement]
