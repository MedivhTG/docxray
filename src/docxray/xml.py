"""Base module of an XML-element/functions in project"""

from collections.abc import Iterator, Mapping
from typing import Any, TypeVar

from lxml import etree

BASE_ELM_T = TypeVar("BASE_ELM_T", bound="BaseOxmlElement")


class BaseOxmlElement(etree.ElementBase):
    """Base XML-element for project (inherits from lxml `ElementBase`), provides type hints."""

    def xpath(self, xpath: str, ns: dict[str, str] | None = None) -> Any:  # type: ignore[override]
        return super().xpath(xpath, namespaces=ns)

    def get_parent(self, elm_hint: type[BASE_ELM_T]) -> BASE_ELM_T | None:
        # Cache parent for styles
        if not hasattr(self, "_parent"):
            self._parent = self.getparent()
        return self._parent  # type: ignore[return-value]

    def iter_find(
        self,
        elm_qn: str,
        elm_hint: type[BASE_ELM_T],
        namespaces: Mapping[str, str] | None = None,
    ) -> Iterator[BASE_ELM_T]:
        return self.iterfind(elm_qn, namespaces)  # type: ignore[return-value]

    def iter_children(
        self,
        elm_qn: str,
        elm_hint: type[BASE_ELM_T],
    ) -> Iterator[BASE_ELM_T]:
        return self.iterchildren(elm_qn)  # type: ignore[return-value]

    def find_first(
        self,
        elm_qn: str,
        elm_hint: type[BASE_ELM_T],
        namespaces: Mapping[str, str] | None = None,
    ) -> BASE_ELM_T | None:
        return self.find(elm_qn, namespaces)  # type: ignore[return-value]

    def find_all(
        self,
        elm_qn: str,
        elm_hint: type[BASE_ELM_T],
        namespaces: Mapping[str, str] | None = None,
    ) -> list[BASE_ELM_T]:
        return self.findall(elm_qn, namespaces)  # type: ignore[return-value]

    def __repr__(self) -> str:
        """Repsentation of an xml-element for debug."""
        return (
            super().__repr__().replace("Element", self.__class__.__name__, 1)
        )


def elm_ns_cls_lookup(
    fallback_cls: type[BaseOxmlElement] = BaseOxmlElement,
) -> etree.ElementNamespaceClassLookup:
    """Get lookup with fallback cls of an `BaseOxmlElement` or given param.

    Args:
        default_element_class (type[BaseOxmlElement], optional): Fallback cls. Defaults to BaseOxmlElement.

    Returns:
        etree.ElementNamespaceClassLookup: `ElementNamespaceClassLookup` instance.
    """
    lookup: etree.ElementNamespaceClassLookup = (
        etree.ElementNamespaceClassLookup()
    )
    fallback = etree.ElementDefaultClassLookup(element=fallback_cls)
    lookup.set_fallback(fallback)
    return lookup
