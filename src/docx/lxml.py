from collections.abc import Mapping
from typing import Any, Self, TypeVar

from lxml import etree

ELM_T = TypeVar("ELM_T", bound="BaseOxmlElement")


class BaseOxmlElement(etree.ElementBase):
    def xpath(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, xpath_qn: str
    ) -> Any:
        return super().xpath(xpath_qn)

    def findall(  # type: ignore[override]
        self,
        path: str,
        elm_hint: type[ELM_T],
        namespaces: Mapping[str, str] | None = None,
    ) -> list[ELM_T]:
        return super().findall(
            path, namespaces
        )  # pyright: ignore[reportReturnType]

    def __repr__(self) -> str:
        return (
            super().__repr__().replace("Element", self.__class__.__name__, 1)
        )


def elm_ns_cls_lookup(
    default_element_class: type[etree.ElementBase] = etree.ElementBase,
) -> etree.ElementNamespaceClassLookup:
    lookup: etree.ElementNamespaceClassLookup = (
        etree.ElementNamespaceClassLookup()
    )
    fallback = etree.ElementDefaultClassLookup(element=default_element_class)
    lookup.set_fallback(fallback)
    return lookup
