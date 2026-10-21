"""Main module for creating XML-elements"""

from __future__ import annotations

from typing import ClassVar

from lxml import etree
from typing_extensions import Sentinel

from .exceptions import OxmlAttrRequiredError

MISSING = Sentinel("MISSING")


def elm_ns_cls_lookup(
    fallback_elm: type[etree.ElementBase] = etree.ElementBase,
) -> etree.ElementNamespaceClassLookup:
    nslookup: etree.ElementNamespaceClassLookup = (
        etree.ElementNamespaceClassLookup()
    )
    nsfallback = etree.ElementDefaultClassLookup(element=fallback_elm)
    nslookup.set_fallback(nsfallback)
    return nslookup


def oxml_parser(
    nslookup_fallback_elm: type[BaseOxmlElement],
) -> etree.XMLParser:
    xml_parser = etree.XMLParser(
        remove_blank_text=True, resolve_entities=False
    )
    nslookup = elm_ns_cls_lookup(nslookup_fallback_elm)
    xml_parser.set_element_class_lookup(nslookup)
    return xml_parser


class BaseOxmlElement(etree.ElementBase):
    _nslookup: ClassVar[etree.ElementNamespaceClassLookup | None] = None
    _nsmap: ClassVar[dict[str, str] | None] = None
    _namespace: ClassVar[str | None] = None
    _tagname: ClassVar[str | None] = None
    __qname__: ClassVar[etree.QName | None] = None

    def __init_subclass__(
        cls,
        nslookup: etree.ElementNamespaceClassLookup | None = None,
        nsmap: dict[str, str] | None = None,
        ns: str | None = None,
        tag: str | None = None,
    ) -> None:
        super().__init_subclass__()
        return cls.register_elm(nslookup, nsmap, ns, tag)

    @property
    def qname(self) -> etree.QName:
        if not self.__qname__:
            raise ValueError("No qualified name provided")
        return self.__qname__

    def attr_required(self, name: str, fixed: str | None = None) -> str:
        value = self.get(name, MISSING)
        if value is MISSING:
            raise OxmlAttrRequiredError(
                f"Cannot get required attribute `{name}`"
            )
        if fixed is not None and value != fixed:
            raise OxmlAttrRequiredError(
                f"Value must equals to `{fixed}`, got `{value}`"
            )
        return value  # pyright: ignore[reportReturnType]

    def attr_optional(
        self, name: str, default: str | None = None
    ) -> str | Sentinel:
        value = self.get(name, MISSING)
        if value is MISSING:
            if default is not None:
                return default
            return MISSING
        return value

    @classmethod
    def register_elm(
        cls,
        nslookup: etree.ElementNamespaceClassLookup | None = None,
        nsmap: dict[str, str] | None = None,
        namespace: str | None = None,
        tagname: str | None = None,
    ) -> None:
        cls._nslookup = nslookup
        cls._nsmap = nsmap
        cls._namespace = namespace
        if namespace:
            cls.NAMESPACE = namespace
        cls._tagname = tagname
        if tagname:
            cls.TAG = tagname
        if not (nslookup and nsmap and namespace and tagname):
            return
        uri = nsmap[namespace]
        ns = nslookup.get_namespace(uri)
        ns[tagname] = cls
        cls.__qname__ = etree.QName(uri, tagname)
