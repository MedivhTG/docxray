"""Objects shared by docx modules."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Generic, Self, cast

# docxray stuff
from docxray.oxml.t.parts.story import StoryPart
from docxray.oxml.t.proxy.types import (
    ProvidesStoryPart,
    ProvidesXmlPart,
)
from docxray.oxml.t.types import ELM_T

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart
    from docxray.transform.ruleset import RuleProxy, RuleSet
    from docxray.transform.transformer import TransformMethod


class ElementProxy(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesXmlPart) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self) -> XmlPart:
        return self._parent.part

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.t.parts.document import DocumentPart
        from docxray.transform.transformer import Transformer

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(
            self,
            ruleset,
            cast("RuleProxy", self.__class__.__name__),
            stringify,
            method,
        )


class StoryChild(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesStoryPart) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        return self._element

    @property
    def part(self) -> StoryPart:
        """The package part containing this object."""
        return self._parent.part

    @cached_property
    def prev_sibling(self) -> Self | None:
        sibling_list = self._element.xpath(
            f"preceding-sibling::{self._element.xml_tag_self}[1]"
        )
        if len(sibling_list) == 0:
            return None
        return self.__class__(sibling_list[0], self._parent)

    @cached_property
    def next_sibling(self) -> Self | None:
        sibling_list = self._element.xpath(
            f"following-sibling::{self._element.xml_tag_self}[1]"
        )
        if len(sibling_list) == 0:
            return None
        return self.__class__(sibling_list[0], self._parent)

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.t.parts.document import DocumentPart
        from docxray.transform.transformer import Transformer

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(
            self,
            ruleset,
            cast("RuleProxy", self.__class__.__name__),
            stringify,
            method,
        )


class PropertyPath(str):
    @property
    def prop(self) -> str:
        return self.rsplit(".", 1)[-1]

    @property
    def path_to_prop(self) -> str:
        return self.rsplit(".", 1)[0]

    @property
    def links(self) -> list[str]:
        return self.split(".")

    def join_left(self, left: str) -> PropertyPath:
        return PropertyPath.base(self.prop, f"{left}.{self.path_to_prop}")

    @classmethod
    def base(cls, prop: str, path_to_prop: str = "") -> Self:
        if not path_to_prop:
            return cls(prop)
        return cls(f"{path_to_prop}.{prop}")


class NotFound:
    def __init__(self, obj: Any, path: PropertyPath) -> None:
        self.obj = obj
        self.path = path


def safe_get_prop(obj: Any, path: PropertyPath, optional: bool = True) -> Any:
    """_summary_

    Args:
        obj (Any): _description_
        path (PropertyPath): _description_
        optional (bool, optional): _description_. Defaults to True.

    Returns:
        Any: Python value or `NotFound` if property not found; or
            `optional` set to False and property was `None`.
    """
    if obj is None:
        return NotFound(obj, path)
    current = obj
    for link in path.links:
        if not hasattr(current, link):
            return NotFound(obj, path)
        current = getattr(current, link)
    if current is None:
        if optional:
            return None
        return NotFound(obj, path)
    return current
