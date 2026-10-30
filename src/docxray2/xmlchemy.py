"""Main module for creating XML-elements"""

from __future__ import annotations

from typing import Any, ClassVar, Self, TypeVar

from lxml import etree
from typing_extensions import Sentinel

from .exceptions import OxmlAttrRequiredError
from .xsd.simple_type import SimpleType
from .xsd.st_primitives import XsdAnySimpleType

MISSING = Sentinel("MISSING")
T = TypeVar("T")
FIND_T = TypeVar("FIND_T", bound="BaseOxmlElement")


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

    def __repr__(self) -> str:
        # Now we can watch right cls name in debug
        return super().__repr__().replace("Element", type(self).__name__, 1)

    def attr_required(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,
        fixed: str | None = None,
    ) -> T:
        value = self.get(name, MISSING)
        if value is MISSING:
            raise OxmlAttrRequiredError(
                f"Cannot get required attribute `{name}`"
            )
        if fixed is not None and value != fixed:
            raise OxmlAttrRequiredError(
                f"Cannot get required attribute `{name}`: value must equals to `{fixed}`, got `{value}`"
            )
        return simple_type.validate_schema(
            value  # pyright: ignore[reportArgumentType]
        )

    def attr_optional(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,  # type: ignore[assignment]
        default: str | None = None,
    ) -> T | Sentinel:
        value = self.get(name, MISSING)
        if value is MISSING:
            if default is not None:
                return simple_type.validate_schema(default)
            return MISSING
        return simple_type.validate_schema(
            value  # pyright: ignore[reportArgumentType]
        )

    def zero_or_more(self, element: type[FIND_T]) -> list[FIND_T]:
        return self.findall(
            element.qname(), self._nsmap
        )  # type: ignore[return-value]

    @classmethod
    def qname(cls) -> etree.QName:
        if not cls.__qname__:
            raise ValueError("No qualified name provided")
        return cls.__qname__

    @classmethod
    def parse(cls, text: str | bytes, parser: etree.XMLParser) -> Self:
        return etree.fromstring(text, parser)  # type: ignore[return-value]

    @classmethod
    def register_elm(
        cls,
        nslookup: etree.ElementNamespaceClassLookup | None = None,
        nsmap: dict[str, str] | None = None,
        namespace: str | None = None,
        tagname: str | None = None,
    ) -> None:
        if nslookup:
            cls._nslookup = nslookup
        if nsmap:
            cls._nsmap = nsmap
        if namespace:
            cls._namespace = namespace
            cls.NAMESPACE = namespace
        if tagname:
            cls._tagname = tagname
            cls.TAG = tagname
        if not (
            cls._nslookup and cls._nsmap and cls._namespace and cls._tagname
        ):
            return
        uri = cls._nsmap[cls._namespace]
        ns = cls._nslookup.get_namespace(uri)
        ns[cls._tagname] = cls
        cls.__qname__ = etree.QName(uri, cls._tagname)


class AttrRequired[T]:
    def __init__(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,
        fixed: str | None = None,
    ) -> None:
        self.name = name
        self.simple_type = simple_type
        self.fixed = fixed

    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.attr_name = name

    def __get__(
        self, instance: BaseOxmlElement | None, owner: type | None = None
    ) -> T:
        if instance is None:
            return self  # type: ignore[return-value]
        return instance.attr_required(self.name, self.simple_type, self.fixed)

    def __set__(self, instance: BaseOxmlElement | None, value: Any) -> None:
        if instance is None:
            return None
        instance.set(self.name, value)
        try:
            instance.attr_required(self.name, self.simple_type, self.fixed)
        except Exception as e:
            instance.attrib.pop(self.name)
            raise OxmlAttrRequiredError(
                f"Cannot set attribute `{self.name}`: `{e}`"
            )


def elm_ns_cls_lookup(
    fallback_elm: type[BaseOxmlElement] = BaseOxmlElement,
) -> etree.ElementNamespaceClassLookup:
    nslookup: etree.ElementNamespaceClassLookup = (
        etree.ElementNamespaceClassLookup()
    )
    nsfallback = etree.ElementDefaultClassLookup(element=fallback_elm)
    nslookup.set_fallback(nsfallback)
    return nslookup
