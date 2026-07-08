"""Objects shared by docx modules."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Generic, Self, cast

# docxray stuff
from docxray.oxml.t.package import TransitionalPackage
from docxray.oxml.t.parts.story import StoryPart
from docxray.oxml.t.proxy.types import (
    ProvidesStoryPart,
    ProvidesXmlPart,
)
from docxray.oxml.t.types import ELM_T

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart
    from docxray.oxml.t.parts.document import DocumentPart
    from docxray.oxml.t.proxy.styles.style import (
        CharacterStyle,
        NumberingStyle,
    )
    from docxray.transform.ruleset import RuleProxy, RuleSet
    from docxray.transform.transformer import TransformMethod


class ElementProxy(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesXmlPart) -> None:
        self._element = element
        self._parent = parent

    @cached_property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @cached_property
    def part(self) -> XmlPart:
        return self._parent.part

    @cached_property
    def document_part(self) -> DocumentPart:
        return document_part(self)

    def path(self, path_str: str) -> PropertyPath:
        return PropertyPath(path_str)

    def prop(self, path: str, optional: bool = False) -> Any:
        """Get property from current element of an proxy."""
        return safe_get_prop(self.element, self.path(path), optional)

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        return transform(self, ruleset, stringify, method)


class StoryChild(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesStoryPart) -> None:
        self._element = element
        self._parent = parent

    @cached_property
    def element(self) -> ELM_T:
        return self._element

    @cached_property
    def part(self) -> StoryPart:
        """The package part containing this object."""
        return self._parent.part

    @cached_property
    def document_part(self) -> DocumentPart:
        return document_part(self)

    def path(self, path_str: str) -> PropertyPath:
        return PropertyPath(path_str)

    def prop(self, path: str, optional: bool = False) -> Any:
        """Get property from current element of an proxy."""
        return safe_get_prop(self.element, self.path(path), optional)

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
        return transform(self, ruleset, stringify, method)


class PropertyPath(str):
    @property
    def end_name(self) -> str:
        return self.rsplit(".", 1)[-1]

    @property
    def base_path(self) -> str:
        return self.rsplit(".", 1)[0]

    @property
    def links(self) -> list[str]:
        return self.split(".")


class NotFound:
    def __init__(self, obj: Any, path: PropertyPath | str) -> None:
        self.obj = obj
        self.path = path


def safe_get_prop(obj: Any, path: PropertyPath, optional: bool = True) -> Any:
    """Get property from object with dot-notation, e.g. `rPr.i.val`.

    Args:
        obj (Any): Given object for getting property.
        path (PropertyPath): Path to property.
        optional (bool, optional): If end-name property not found return
            `None` instead of `NotFound`. Defaults to True.

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


def document_part(proxy: ElementProxy | StoryChild) -> DocumentPart:
    return cast("TransitionalPackage", proxy.part.package).main_document_part


def transform(
    proxy: ElementProxy | StoryChild,
    ruleset: RuleSet | None = None,
    stringify: bool = True,
    method: TransformMethod = "html",
) -> Any:
    # docxray stuff
    from docxray.transform.transformer import Transformer

    ruleset = ruleset or proxy.document_part._default_html_ruleset
    return Transformer.transform(
        proxy,
        ruleset,
        cast("RuleProxy", proxy.__class__.__name__),
        stringify,
        method,
    )


def from_style_inheritance(
    proxy: ElementProxy | StoryChild,
    style: CharacterStyle | NumberingStyle,
    path: str,
    optional: bool = False,
) -> Any:
    """Iterate over style hierarchy with same style from given to get property value.

    Args:
        proxy (ElementProxy | StoryChild): Proxy to get styles.
        style (CharacterStyle | NumberingStyle): Given style.
        path (str): Path to an element in element tree.
        optional (bool, optional): If endname property can be `None` and you
            won't get `NotFound` instance instead. Defaults to False.

    Returns:
        Any: `NotFound` instance or Any value.
    """
    val = NotFound(style, path)
    while isinstance(val, NotFound):
        val = safe_get_prop(style.element, proxy.path(path), optional)
        base_style = proxy.document_part.styles.base_style(style)
        if not isinstance(base_style, style.__class__):
            return val
        style = base_style
    return val


def from_doc_dflts(
    proxy: ElementProxy | StoryChild,
    path: str,
    optional: bool = False,
) -> Any:
    """Get property value directly from document deafults in styles.

    Args:
        proxy (ElementProxy | StoryChild): Proxy to get styles.
        path (PropertyPath): Path to an element in element tree.
        optional (bool, optional): If endname property can be `None` and you
            won't get `NotFound` instance instead. Defaults to False.

    Returns:
        Any: `NotFound` instance or Any value.
    """
    doc_dflts = proxy.document_part.styles.document_defaults
    if doc_dflts is None:
        return NotFound(proxy, path)
    return doc_dflts.prop(path, optional)
