"""Main module for parsing/getting XML nodes from tree."""

from copy import deepcopy
from functools import cached_property
from typing import Any, TypeVar

from lxml.etree import QName

# docxray stuff
from docxray.enum.lxml import POS
from docxray.exceptions import InvalidXmlError
from docxray.lxml import BaseOxmlElement
from docxray.xsd.primitives import XsdString
from docxray.xsd.xsd import XsdPrimitive, XsdSimpleType

from .ns import nsmap
from .types import ELM_T

ST_T = TypeVar("ST_T", bound=XsdSimpleType | XsdPrimitive)
T = TypeVar("T")

nsmap_reversed = {v: k for k, v in nsmap.items()}


class OxmlElement(BaseOxmlElement):
    def xpath(self, xpath: str) -> Any:  # type: ignore[override]
        return super().xpath(xpath, nsmap)

    @cached_property
    def is_first(self) -> bool:
        """XML-node has no siblings with same tage before."""
        return self.xpath(f"not(preceding-sibling::{self.xml_tag_self})")

    @cached_property
    def is_last(self) -> bool:
        """XML-node has no siblings with same tage after."""
        return self.xpath(f"not(following-sibling::{self.xml_tag_self})")

    @cached_property
    def xml_pos(self) -> POS:
        """XML-postion relative to it's siblings."""
        return self.xml_position(self.is_first, self.is_last)

    @cached_property
    def xml_tag_self(self) -> str:
        """Self tag name with prefix"""
        return self.xml_tag(self.tag)

    def xml_tag(self, qn_tag: Any) -> str:
        """Get tag name with prefix, e.g. `w:p` for `{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p` (clark-notation).

        Args:
            qn_tag (Any): Tag in clark-notation.

        Raises:
            InvalidXmlError: If cannot recognize namespace from mapping.

        Returns:
            str: Tag name string.
        """
        qn = QName(qn_tag)
        if qn.namespace is None:
            msg = "No namespace provided for word element"
            raise InvalidXmlError(msg)
        return f"{nsmap_reversed[qn.namespace]}:{qn.localname}"

    def attr_optional(
        self,
        elm_qn: str,
        simple_type: type[ST_T] | None = None,
        default: Any = None,
        **facets: Any,
    ) -> Any:
        """Get optional attribute from element with XSD validation.

        Args:
            elm_qn (str): Qalified name of an desired element.
            simple_type (type[ST_T] | None, optional): Validation XSD cls type on found element. Defaults to None.
            default (Any, optional): Default value if element not found. Defaults to None.

        Returns:
            Any: Validated and converted attribute value.
        """
        attr = self.get(elm_qn)
        if attr is None:
            return default
        if simple_type is None:
            return XsdString.validate(attr, **facets)
        if issubclass(simple_type, XsdPrimitive):
            return simple_type.validate(attr, **facets)
        return simple_type(attr).validate()

    def attr_required(
        self, elm_qn: str, simple_type: type[ST_T], **facets: dict[str, Any]
    ) -> Any:
        """Get required attribute from element with XSD validation.

        Args:
            elm_qn (str): Qalified name of an desired element.
            simple_type (type[ST_T]): Validation XSD cls type on found element.

        Raises:
            InvalidXmlError: If required lement is not found.

        Returns:
            Any: Validated and converted attribute value.
        """
        attr = self.get(elm_qn)
        if attr is None:
            msg = (
                f"Attribute {elm_qn} was None when one was required for {self}"
            )
            raise InvalidXmlError(msg)
        if issubclass(simple_type, XsdPrimitive):
            return simple_type.validate(attr, **facets)
        return simple_type(attr).validate()

    def child_exactly_one(self, elm_qn: str, elm_hint: type[ELM_T]) -> ELM_T:
        """Get child with `minOccurs=1` and `maxOccurs=1`.

        Args:
            elm_qn (str): Qualified name of element tag (clark-notation).
            elm_hint (type[ELM_T]): Element cast hint returned.

        Raises:
            InvalidXmlError: If child not found.
            InvalidXmlError: If child appears more than 1 times.

        Returns:
            ELM_T: OxmlElement found.
        """
        iterator = self.iterfind(elm_qn, elm_hint)
        child = next(iterator, None)
        if child is None:
            msg = f"Child {elm_qn} was None when one was required for {self}"
            raise InvalidXmlError(msg)
        child_ahead = next(iterator, None)
        if child_ahead is not None:
            msg = f"Child {elm_qn} must appear only once for {self}"
            raise InvalidXmlError(msg)
        return child

    def child_zero_or_one(
        self, elm_qn: str, elm_hint: type[ELM_T]
    ) -> ELM_T | None:
        """Get child with `minOccurs=0` and `maxOccurs=1`.

        Args:
            elm_qn (str): Qualified name of element tag (clark-notation).
            elm_hint (type[ELM_T]): Element cast hint returned.

        Raises:
            InvalidXmlError: If child appears more than 1 times.

        Returns:
            ELM_T | None: OxmlElement found or not.
        """
        iterator = self.iterfind(elm_qn, elm_hint)
        child = next(iterator, None)
        if child is None:
            return None
        child_ahead = next(iterator, None)
        if child_ahead is not None:
            msg = f"Child {elm_qn} must appear 0 or 1 time for {self}"
            raise InvalidXmlError(msg)
        return child

    def child_zero_or_more(
        self, elm_qn: str, elm_hint: type[ELM_T]
    ) -> list[ELM_T]:
        """Get children with `minOccurs=0` and `maxOccurs=*`.

        Args:
            elm_qn (str): Qualified name of element tag (clark-notation).
            elm_hint (type[ELM_T]): Element cast hint returned.

        Returns:
            list[ELM_T]: List of Oxmlelement's found.
        """
        return self.findall(elm_qn, elm_hint)

    def child_zero_or_n(
        self, elm_qn: str, elm_hint: type[ELM_T], max_occurs: int
    ) -> list[ELM_T]:
        """Get children with `minOccurs=0` and `maxOccurs=custom`

        Args:
            elm_qn (str): Qualified name of element tag (clark-notation).
            elm_hint (type[ELM_T]): Element cast hint returned.
            max_occurs (int): Maximum of found children.

        Raises:
            InvalidXmlError: When iteration exceeded the `max_occurs`.

        Returns:
            list[ELM_T]: List of Oxmlelement's found.
        """
        count = 0
        children: list[ELM_T] = []
        iterator = self.iterfind(elm_qn, elm_hint)
        while count <= max_occurs:
            child = next(iterator, None)
            if child is None:
                return children
            count += 1
            children.append(child)
        msg = (
            f"Children {elm_qn} iteration exceeded the maximum of {max_occurs}"
        )
        raise InvalidXmlError(msg)

    def recreate(self, cls: type[ELM_T]) -> ELM_T:
        """Get copy of current element with change cls type.

        Usually needed in edge cases where ECMA schema uses same element with different XSD types,
        e.g. `w:spacing` for `CT_Spacing` and `CT_SignedTwipsMeasure`.

        Args:
            cls (type[ELM_T]): `OxmlElement` cls for change.

        Returns:
            ELM_T: Copy of and current element.
        """
        new_elm = deepcopy(self)
        new_elm.__class__ = cls  # pyright: ignore[reportAttributeAccessIssue]
        return new_elm  # type: ignore[return-value]

    @classmethod
    def xml_position(cls, is_first: bool, is_last: bool) -> POS:
        """Determine XML position relative to it's siblings.

        Args:
            is_first (bool): F
            is_last (bool): _description_

        Returns:
            POS: _description_
        """
        if not is_first and not is_last:
            return POS.MIDDLE
        if is_first and not is_last:
            return POS.START
        if not is_first and is_last:
            return POS.END
        return POS.ONE_ITEM
