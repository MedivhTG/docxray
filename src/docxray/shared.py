"""Objects shared by docx modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Self

# docxray stuff
from docxray.parts.story import StoryPart
from docxray.types import ELM_T, ProvidesStoryPart, ProvidesXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart


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


def safe_get_prop(
    obj: Any, prop_path: PropertyPath, default: Any = None
) -> Any:
    """Get property from object by path safely.

    Args:
        obj (Any): From python ojbect.
        prop_path (PropertyPath): Property path like `rPr.i`
        default (Any, optional): Return default if cannot get property
            on path. Defaults to None.

    Returns:
        Any: Value from property or default.
    """
    current = obj
    for link in prop_path.links:
        if not hasattr(current, link):
            return default
        current = getattr(current, link)
    return current
