"""Main module for creating XML-elements"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, ClassVar, Self, TypeVar
from warnings import warn

from lxml import etree
from typing_extensions import Sentinel

from .exceptions import (
    OxmlAttrOptionalError,
    OxmlAttrRequiredError,
    OxmlContentError,
)
from .xsd.exceptions import XsdValidationError
from .xsd.simple_type import SimpleType
from .xsd.st_primitives import XsdAnySimpleType

MISSING = Sentinel("MISSING")
T = TypeVar("T")
FIND_T = TypeVar("FIND_T", bound="BaseOxmlElement")


class BaseOxmlElement(etree.ElementBase):
    """Base class for all OXML elements.

    Subclasses declare their XML identity via class kwargs
    (``nslookup=``, ``nsmap=``, ``ns=``, ``tag=``) which are forwarded to
    ``register_elm``; once the namespace lookup, nsmap, namespace and tag are
    all known, the class is registered in ``nslookup`` and its QName is
    computed. Attribute access is provided by ``attr_required`` /
    ``attr_optional``, which read and validate values through ``SimpleType``.
    """

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
        cls.register_elm(nslookup, nsmap, ns, tag)

    def __repr__(self) -> str:
        # Now we can watch right cls name in debug
        return super().__repr__().replace("Element", type(self).__name__, 1)

    def attr_required(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,  # type: ignore[assignment]
        fixed: str | None = None,
    ) -> T:
        """Read a required attribute and validate it.

        Args:
            name (str): Attribute name.
            simple_type (type[SimpleType[T]]): Type used to validate and
                convert the raw XML value. Defaults to ``XsdAnySimpleType``.
            fixed (str | None): Optional raw XML value (a string) that the
                stored attribute must equal exactly. Defaults to ``None``.

        Returns:
            T: Converted attribute value.

        Raises:
            OxmlAttrRequiredError: If the attribute is missing or its raw XML
                value does not equal ``fixed``.
            XsdValidationError: If validation by ``simple_type`` fails.
        """
        value = self.get(name, MISSING)
        if value is MISSING:
            raise OxmlAttrRequiredError(
                f"Cannot get required attribute `{name}` from `{self.__class__}`: missing"
            )
        if fixed is not None and value != fixed:
            raise OxmlAttrRequiredError(
                f"Cannot get required attribute `{name}` from `{self.__class__}`: value must equals to `{fixed}`, got `{value}`"
            )
        return simple_type.validate_schema(
            value  # pyright: ignore[reportArgumentType]
        )

    def attr_optional(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,  # type: ignore[assignment]
        default: str | None = None,
    ) -> T | None:
        """Read an optional attribute and validate it.

        Args:
            name (str): Attribute name.
            simple_type (type[SimpleType[T]]): Type used to validate and
                convert the raw XML value. Defaults to ``XsdAnySimpleType``.
            default (str | None): Optional raw XML value (a string) to
                validate and return when the attribute is absent. Defaults to
                ``None``.

        Returns:
            T | None: Converted attribute value; the converted ``default`` if
            the attribute is absent; or ``None`` if both are absent.

        Raises:
            XsdValidationError: If validation by ``simple_type`` fails.
        """
        value = self.get(name, MISSING)
        if value is MISSING:
            if default is not None:
                return simple_type.validate_schema(default)
            return None
        return simple_type.validate_schema(
            value  # pyright: ignore[reportArgumentType]
        )

    def tag_content(
        self, simple_type: type[SimpleType[T]] = XsdAnySimpleType  # type: ignore[assignment]
    ) -> T | None:
        content = self.text
        if content is None:
            return None
        return simple_type.validate_schema(content)

    def zero_or_more(self, element: type[FIND_T]) -> list[FIND_T]:
        """Return all direct children matching ``element``'s QName.

        Args:
            element (type[FIND_T]): Element class whose QName is matched.

        Returns:
            list[FIND_T]: Matching child elements.
        """
        return self.findall(
            element.qname(), self._nsmap
        )  # type: ignore[return-value]

    def zero_or_one(self, element: type[FIND_T]) -> FIND_T | None:
        iterator = self.iterfind(element.qname())
        found_elm = next(iterator, None)
        if found_elm is None:
            return None
        found_ahead = next(iterator, None)
        if found_ahead is None:
            return found_elm  # type: ignore[return-value]
        warn(f"Child element `{element.qname()}` must appear once!")
        while found_ahead is not None:
            found_ahead_next = next(iterator, None)
            if found_ahead_next is None:
                break
            found_ahead = found_ahead_next
        return found_ahead  # type: ignore[return-value]

    @classmethod
    def qname(cls) -> etree.QName:
        """Return the element's qualified name.

        Returns:
            etree.QName: Qualified name (namespace URI + local tag).

        Raises:
            ValueError: If the class was never fully registered.
        """
        if not cls.__qname__:
            raise ValueError("No qualified name provided")
        return cls.__qname__

    @classmethod
    def parse(cls, text: str | bytes, parser: etree.XMLParser) -> Self:
        """Parse XML text into an instance of this element class.

        Args:
            text (str | bytes): XML source.
            parser (etree.XMLParser): Parser configured with the appropriate
                class lookup.

        Returns:
            Self: Parsed element.
        """
        return etree.fromstring(text, parser)  # type: ignore[return-value]

    @classmethod
    @abstractmethod
    def from_xml(cls, text: str | bytes) -> Self: ...

    @classmethod
    def register_elm(
        cls,
        nslookup: etree.ElementNamespaceClassLookup | None = None,
        nsmap: dict[str, str] | None = None,
        namespace: str | None = None,
        tagname: str | None = None,
    ) -> None:
        """Store element identity and register the class in the namespace.

        Each argument is applied only if truthy; registration and QName
        computation happen once all four pieces (``nslookup``, ``nsmap``,
        ``namespace``, ``tagname``) are known.

        Args:
            nslookup (etree.ElementNamespaceClassLookup | None): Namespace
                lookup to register into. Defaults to ``None``.
            nsmap (dict[str, str] | None): Prefix → URI map. Defaults to
                ``None``.
            namespace (str | None): Namespace prefix. Defaults to ``None``.
            tagname (str | None): Local tag name. Defaults to ``None``.
        """
        if nslookup:
            cls._nslookup = nslookup
        if nsmap:
            cls._nsmap = nsmap
        if namespace:
            cls._namespace = namespace
        if tagname:
            cls._tagname = tagname
        if not (
            cls._nslookup and cls._nsmap and cls._namespace and cls._tagname
        ):
            return
        uri = cls._nsmap[cls._namespace]
        ns = cls._nslookup.get_namespace(uri)
        ns[cls._tagname] = cls
        cls.__qname__ = etree.QName(uri, cls._tagname)


class AttrRequired[T]:
    """Descriptor for a required, XSD-validated attribute.

    Reading delegates to ``attr_required``; writing sets the attribute and
    re-validates it, rolling back on failure.

    Attributes:
        name (str): Attribute name.
        simple_type (type[SimpleType[T]]): Type used for validation.
        fixed (str | None): Optional raw XML value (a string) the attribute
            must equal exactly.
    """

    __slots__ = ("fixed", "name", "simple_type")

    def __init__(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,  # type: ignore[assignment]
        fixed: str | None = None,
    ) -> None:
        self.name = name
        self.simple_type = simple_type
        self.fixed = fixed

    def __get__(
        self, element: BaseOxmlElement | None, owner: type | None = None
    ) -> T:
        if element is None:
            return self  # type: ignore[return-value]
        return element.attr_required(self.name, self.simple_type, self.fixed)

    def __set__(self, element: BaseOxmlElement | None, value: Any) -> None:
        if element is None:
            return
        old_value = element.get(self.name, MISSING)
        element.set(self.name, value)
        try:
            element.attr_required(self.name, self.simple_type, self.fixed)
        except (OxmlAttrRequiredError, XsdValidationError) as e:
            if old_value is MISSING:
                element.attrib.pop(self.name)
            else:
                element.set(
                    self.name, old_value  # pyright: ignore[reportArgumentType]
                )
            raise OxmlAttrRequiredError(
                f"Cannot set required attribute `{self.name}` to `{element.__class__}`: `{e}`"
            )


class AttrOptional[T]:
    """Descriptor for an optional, XSD-validated attribute.

    Reading delegates to ``attr_optional``; writing sets the attribute and
    re-validates it, rolling back on failure.

    Attributes:
        name (str): Attribute name.
        simple_type (type[SimpleType[T]]): Type used for validation.
        default (str | None): Optional raw XML value (a string) validated and
            returned when the attribute is absent.
    """

    __slots__ = ("default", "name", "simple_type")

    def __init__(
        self,
        name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,  # type: ignore[assignment]
        default: str | None = None,
    ) -> None:
        self.name = name
        self.simple_type = simple_type
        self.default = default

    def __get__(
        self, element: BaseOxmlElement | None, owner: type | None = None
    ) -> T | None:
        if element is None:
            return self  # type: ignore[return-value]
        return element.attr_optional(self.name, self.simple_type, self.default)

    def __set__(self, element: BaseOxmlElement | None, value: Any) -> None:
        if element is None:
            return
        old_value = element.get(self.name, MISSING)
        element.set(self.name, value)
        try:
            element.attr_optional(self.name, self.simple_type, self.default)
        except XsdValidationError as e:
            if old_value is MISSING:
                element.attrib.pop(self.name)
            else:
                element.set(
                    self.name, old_value  # pyright: ignore[reportArgumentType]
                )
            raise OxmlAttrOptionalError(
                f"Cannot set optional attribute `{self.name}` to `{element.__class__}`: `{e}`"
            )


class Content[T]:
    __slots__ = ("simple_type",)

    def __init__(
        self,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType,  # type: ignore[assignment]
    ) -> None:
        self.simple_type = simple_type

    def __get__(
        self, element: BaseOxmlElement | None, owner: type | None = None
    ) -> T | None:
        if element is None:
            return self  # type: ignore[return-value]
        return element.tag_content(self.simple_type)

    def __set__(self, element: BaseOxmlElement | None, value: Any) -> None:
        if element is None:
            return
        old_value = element.text
        element.text = value
        try:
            element.tag_content(self.simple_type)
        except XsdValidationError as e:
            element.text = old_value
            raise OxmlContentError(
                f"Cannot set content (text) to `{element.__class__}`: `{e}`"
            )


def elm_ns_cls_lookup(
    fallback_elm: type[BaseOxmlElement] = BaseOxmlElement,
) -> etree.ElementNamespaceClassLookup:
    """Build a namespace-aware class lookup with a default fallback.

    Args:
        fallback_elm (type[BaseOxmlElement]): Element class used for unknown
            namespaces/tags. Defaults to ``BaseOxmlElement``.

    Returns:
        etree.ElementNamespaceClassLookup: Lookup ready to be passed as
        ``nslookup=`` to element subclasses.
    """
    nslookup: etree.ElementNamespaceClassLookup = (
        etree.ElementNamespaceClassLookup()
    )
    nsfallback = etree.ElementDefaultClassLookup(element=fallback_elm)
    nslookup.set_fallback(nsfallback)
    return nslookup
