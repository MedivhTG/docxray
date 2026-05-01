from collections.abc import Mapping
from typing import Any, TypeVar

from lxml import etree

BASE_ELM_T = TypeVar("BASE_ELM_T", bound="BaseOxmlElement")


class BaseOxmlElement(etree.ElementBase):
    def xpath(self, xpath_qn: str) -> Any:  # type: ignore[override]
        return super().xpath(xpath_qn)

    def find(  # type: ignore[override]
        self,
        path: str,
        elm_hint: type[BASE_ELM_T],
        namespaces: Mapping[str, str] | None = None,
    ) -> BASE_ELM_T | None:
        return super().find(path, namespaces)  # type: ignore[return-value]

    def findall(  # type: ignore[override]
        self,
        path: str,
        elm_hint: type[BASE_ELM_T],
        namespaces: Mapping[str, str] | None = None,
    ) -> list[BASE_ELM_T]:
        return super().findall(path, namespaces)  # type: ignore[return-value]

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
