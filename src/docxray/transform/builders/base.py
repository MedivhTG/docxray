from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from lxml.html import HtmlElement

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet

T = TypeVar("T")


class HtmlBuilder(Generic[T]):
    @classmethod
    @abstractmethod
    def element(cls, proxy: T, ruleset: RuleSet) -> HtmlElement: ...
