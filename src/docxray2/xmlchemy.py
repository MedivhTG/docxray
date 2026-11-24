"""Main module for creating XML-elements"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, ClassVar, Literal, Self, TypeVar

from lxml import etree
from typing_extensions import Sentinel

from .exceptions import (
    OxmlAttrOptionalError,
    OxmlAttrRequiredError,
    OxmlChoiceManyAtLeastOneError,
    OxmlChoiceOneError,
    OxmlContentError,
    OxmlExactlyOneError,
)
from .xsd.exceptions import XsdStringifyError, XsdValidationError
from .xsd.primitives import XsdAnySimpleType
from .xsd.simple_type import SimpleType

MISSING = Sentinel("MISSING")
T = TypeVar("T")
ELM_T = TypeVar("ELM_T", bound="BaseOxmlElement")

type Nsmap = dict[str | None, str]
type NsmapMode = Literal["single_ns_no_prefix", "single_ns", "full_nsmap"]
type Attrib = dict[str | etree.QName, Any]


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
    _nsmap: ClassVar[Nsmap | None] = None
    _namespace: ClassVar[str | None] = None
    _tagname: ClassVar[str | None] = None
    _qname: ClassVar[etree.QName | None] = None
    _attrs: ClassVar[dict[str, Attr] | None] = None

    class _Registry:
        _attrs_map: dict[type[BaseOxmlElement], dict[str, Attr]] = {}

        @classmethod
        def attrs(cls, elm_cls: type[BaseOxmlElement]) -> dict[str, Attr]:
            merged: dict[str, Attr] = {}
            for base in reversed(elm_cls.__mro__):
                merged.update(cls._attrs_map.get(base, {}))
            return merged

        @classmethod
        def register_attr(
            cls, elm_cls: type[BaseOxmlElement], name: str, attr: Attr
        ) -> None:
            attr_map = cls._attrs_map.get(elm_cls)
            if attr_map:
                attr_map[name] = attr
            else:
                cls._attrs_map[elm_cls] = {name: attr}

    def __init_subclass__(
        cls,
        nslookup: etree.ElementNamespaceClassLookup | None = None,
        nsmap: Nsmap | None = None,
        ns: str | None = None,
        tag: str | None = None,
    ) -> None:
        super().__init_subclass__()
        cls._register_elm(nslookup, nsmap, ns, tag)
        cls._register_attrs()

    def __repr__(self) -> str:
        # Now we can watch right cls name in debug
        return super().__repr__().replace("Element", type(self).__name__, 1)

    def tag_content(
        self, simple_type: type[SimpleType[T]] = XsdAnySimpleType[str]  # type: ignore[assignment]
    ) -> T | None:
        content = self.text
        if content is None:
            return None
        return simple_type.validate_schema(content)

    def tag_full_content(self, simple_type: type[SimpleType[T]] = XsdAnySimpleType[str]) -> T:  # type: ignore[assignment]
        full_content = "".join(self.itertext())
        return simple_type.validate_schema(full_content)

    def all(self, element: type[ELM_T]) -> list[ELM_T]:
        """Return all direct children matching ``element``'s QName.

        Args:
            element (type[FIND_T]): Element class whose QName is matched.

        Returns:
            list[FIND_T]: Matching child elements.
        """
        return list(self.iterchildren(element.qname()))  # type: ignore[arg-type]

    def one_or_none(self, element: type[ELM_T]) -> ELM_T | None:
        return next(self.iterchildren(element.qname(), reversed=True), None)  # type: ignore[return-value]

    def one(self, element: type[ELM_T]) -> ELM_T:
        found_elm = next(
            self.iterchildren(element.qname(), reversed=True), None
        )
        if found_elm is None:
            raise OxmlExactlyOneError(
                f"Must be at least one element: `{element.qname()}`!"
            )
        return found_elm  # type: ignore[return-value]

    def choice_one(self, *choices: type[ELM_T]) -> ELM_T:
        found_elm = next(
            self.iterchildren(*[ch.qname() for ch in choices], reversed=True),
            None,
        )
        if found_elm is None:
            raise OxmlChoiceOneError(
                f"Must be at least one chosen element: `{[e.qname() for e in choices]}`"
            )
        return found_elm  # type: ignore[return-value]

    def choice_many_at_least_one(self, *choices: type[ELM_T]) -> list[ELM_T]:
        found_lst = list(self.iterchildren(*[ch.qname() for ch in choices]))
        if not found_lst:
            raise OxmlChoiceManyAtLeastOneError(
                f"Must be at least one chosen element in choice list: `{[e.qname() for e in choices]}`"
            )
        return found_lst  # type: ignore[return-value]

    def to_string(self) -> bytes:
        return etree.tostring(self)

    def append_child(self, element: BaseOxmlElement) -> None:
        return self.append(element)  # pyright: ignore[reportArgumentType]

    def insert_child(self, index: int, element: BaseOxmlElement) -> None:
        return self.insert(
            index, element  # pyright: ignore[reportArgumentType]
        )

    def replace_child(
        self, old_element: BaseOxmlElement, new_element: BaseOxmlElement
    ) -> None:
        return self.replace(
            old_element, new_element  # pyright: ignore[reportArgumentType]
        )

    def upsert_child(
        self, old_element: BaseOxmlElement | None, new_element: BaseOxmlElement
    ) -> None:
        if old_element is None:
            self.append_child(new_element)
        else:
            self.replace_child(old_element, new_element)

    def remove_child(self, element: BaseOxmlElement) -> None:
        return self.remove(element)  # pyright: ignore[reportArgumentType]

    def _attr_required(
        self,
        name: str | etree.QName,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType[str],  # type: ignore[assignment]
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

    def _attr_optional(
        self,
        name: str | etree.QName,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType[str],  # type: ignore[assignment]
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

    @classmethod
    def qname(cls) -> etree.QName:
        """Return the element's qualified name.

        Returns:
            etree.QName: Qualified name (namespace URI + local tag).

        Raises:
            ValueError: If the class was never fully registered.
        """
        if not cls._qname:
            raise ValueError("No qualified name provided")
        return cls._qname

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
    def new_element(
        cls,
        *children: BaseOxmlElement,
        parser: etree.XMLParser[ELM_T],
        nsmap_override: Nsmap | None = None,
        nsmap_mode: NsmapMode = "single_ns",
        attrib_update: Attrib | None = None,
    ) -> Self:
        # Create attributes
        attrib: Attrib = {}
        for attr in cls.attributes().values():
            if isinstance(attr, AttrRequired):
                attrib[attr.qname] = (
                    attr.fixed if attr.fixed is not None else ""
                )
        if attrib_update:
            attrib.update(attrib_update)
        # Names
        qname = cls.qname()
        uri = qname.namespace
        # Nsmap init
        if nsmap_override is not None:
            nsmap = nsmap_override
        elif cls._nsmap is not None:
            nsmap = cls._nsmap
        else:
            nsmap = {}
        if nsmap_mode == "single_ns" and cls._namespace in nsmap:
            nsmap = {cls._namespace: nsmap[cls._namespace]}
        elif nsmap_mode == "single_ns_no_prefix" and uri:
            nsmap = {None: uri}
        # Create element
        elm = parser.makeelement(qname, nsmap=nsmap, attrib=attrib)
        # Append children
        for child in children:
            elm.append_child(child)
        # Return
        return elm  # type: ignore[return-value]

    @classmethod
    @abstractmethod
    def new(
        cls,
        *children: BaseOxmlElement,
        nsmap_override: Nsmap,
        nsmap_mode: NsmapMode = "single_ns",
        attrib_update: Attrib | None = None,
    ) -> Self: ...

    @classmethod
    @abstractmethod
    def from_xml(cls, text: str | bytes) -> Self: ...

    @classmethod
    def attributes(cls) -> dict[str, Attr]:
        if cls._attrs is None:
            cls._attrs = {}
        return cls._attrs

    @classmethod
    def _register_elm(
        cls,
        nslookup: etree.ElementNamespaceClassLookup | None = None,
        nsmap: Nsmap | None = None,
        namespace: str | None = None,
        tagname: str | None = None,
    ) -> None:
        cls._nsmap = nsmap if nsmap is not None else cls._resolve_nsmap()
        if tagname:
            cls._tagname = tagname
        if nslookup:
            cls._nslookup = nslookup
        if namespace:
            cls._namespace = namespace
        if not (cls._nslookup and cls._nsmap and cls._tagname):
            return
        uri = cls._nsmap[cls._namespace]
        ns = cls._nslookup.get_namespace(uri)
        ns[cls._tagname] = cls
        cls._qname = etree.QName(uri, cls._tagname)

    @classmethod
    def _resolve_nsmap(cls) -> Nsmap | None:
        for parent_cls in cls.__mro__:
            if not issubclass(parent_cls, BaseOxmlElement):
                continue
            if parent_cls._nsmap:
                return parent_cls._nsmap
        return None

    @classmethod
    def _register_attrs(cls) -> None:
        if cls._qname is not None:
            for attr_name, attr in cls._Registry.attrs(cls).items():
                attr.compute_qname()
                if cls._attrs is None:
                    cls._attrs = {}
                cls._attrs[attr_name] = attr


class Attr:
    def __set_name__(self, owner: type[BaseOxmlElement], name: str) -> None:
        if not issubclass(owner, BaseOxmlElement):
            raise TypeError(
                f"Derived {self.__class__} must be {BaseOxmlElement} subclass!"
            )
        self.owner = owner
        self.name = name
        self._qname: etree.QName | None = None
        owner._Registry.register_attr(owner, name, self)

    def _compute_qname(self, attr_name: str) -> None:
        if self._qname is None and self.owner._nsmap is not None:
            self._qname = qname(self.owner._nsmap, attr_name)

    @abstractmethod
    def compute_qname(self) -> None: ...


class AttrRequired[T](Attr):
    """Descriptor for a required, XSD-validated attribute.

    Reading delegates to ``attr_required``; writing sets the attribute and
    re-validates it, rolling back on failure.

    Attributes:
        name (str): Attribute name.
        simple_type (type[SimpleType[T]]): Type used for validation.
        fixed (str | None): Optional raw XML value (a string) the attribute
            must equal exactly.
    """

    def __init__(
        self,
        attr_name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType[str],  # type: ignore[assignment]
        fixed: str | None = None,
    ) -> None:
        self._attr_name = attr_name
        self.simple_type = simple_type
        self.fixed = fixed

    @property
    def qname(self) -> etree.QName:
        if self._qname is None:
            self._qname = qname(self.owner._nsmap or {}, self._attr_name)
        return self._qname

    def compute_qname(self) -> None:
        self._compute_qname(self._attr_name)

    def __get__(
        self, element: BaseOxmlElement | None, owner: type | None = None
    ) -> T:
        if element is None:
            return self  # type: ignore[return-value]
        return element._attr_required(self.qname, self.simple_type, self.fixed)

    def __set__(self, element: BaseOxmlElement | None, py_value: Any) -> None:
        if element is None:
            return
        if py_value is None:
            raise ValueError("Required attribute cannot be set as None!")
        try:
            xml_value = self.simple_type.stringify(py_value)
            self.simple_type.validate_schema(xml_value)
        except (XsdValidationError, XsdStringifyError) as e:
            raise OxmlAttrRequiredError(
                f"Cannot set required attribute `{self.qname}` to `{element.__class__}`: `{e}`"
            )
        element.set(self.qname, xml_value)


class AttrOptional[T](Attr):
    """Descriptor for an optional, XSD-validated attribute.

    Reading delegates to ``attr_optional``; writing sets the attribute and
    re-validates it, rolling back on failure.

    Attributes:
        name (str): Attribute name.
        simple_type (type[SimpleType[T]]): Type used for validation.
        default (str | None): Optional raw XML value (a string) validated and
            returned when the attribute is absent.
    """

    def __init__(
        self,
        attr_name: str,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType[str],  # type: ignore[assignment]
        default: str | None = None,
    ) -> None:
        self._attr_name = attr_name
        self.simple_type = simple_type
        self.default = default

    @property
    def qname(self) -> etree.QName:
        if self._qname is None:
            self._qname = qname(self.owner._nsmap or {}, self._attr_name)
        return self._qname

    def compute_qname(self) -> None:
        self._compute_qname(self._attr_name)

    def __get__(
        self, element: BaseOxmlElement | None, owner: type | None = None
    ) -> T | None:
        if element is None:
            return self  # type: ignore[return-value]
        return element._attr_optional(
            self.qname, self.simple_type, self.default
        )

    def __set__(self, element: BaseOxmlElement | None, py_value: Any) -> None:
        if element is None:
            return
        if py_value is None:
            element.attrib.pop(self.qname, None)
            return
        try:
            xml_value = self.simple_type.stringify(py_value)
            self.simple_type.validate_schema(xml_value)
        except (XsdValidationError, XsdStringifyError) as e:
            raise OxmlAttrOptionalError(
                f"Cannot set optional attribute `{self.qname}` to `{element.__class__}`: `{e}`"
            )
        element.set(self.qname, xml_value)


class Content[T]:
    __slots__ = ("simple_type",)

    def __init__(
        self,
        simple_type: type[SimpleType[T]] = XsdAnySimpleType[str],  # type: ignore[assignment]
    ) -> None:
        self.simple_type = simple_type

    def __get__(
        self, element: BaseOxmlElement | None, owner: type | None = None
    ) -> T | None:
        if element is None:
            return self  # type: ignore[return-value]
        return element.tag_content(self.simple_type)

    def __set__(self, element: BaseOxmlElement | None, py_value: Any) -> None:
        if element is None:
            return
        if py_value is None:
            element.text = py_value
            return
        try:
            xml_value = self.simple_type.stringify(py_value)
            self.simple_type.validate_schema(xml_value)
        except (XsdValidationError, XsdStringifyError) as e:
            raise OxmlContentError(
                f"Cannot set content (text) to `{element.__class__}`: `{e}`"
            )
        element.text = xml_value


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


def qname(nsmap: Nsmap, qn: str) -> etree.QName:
    tag_parts = qn.split(":")
    if len(tag_parts) == 2:
        tag_root, tag_name = tag_parts
        return etree.QName(nsmap[tag_root], tag_name)
    elif len(tag_parts) == 1:
        return etree.QName(None, tag_parts[0])
    raise ValueError(f"Not parsed tagname: {qn}")
