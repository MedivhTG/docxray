from functools import cached_property
from typing import Any, TypeVar

from lxml.etree import QName

# docxray stuff
from docxray.enum.lxml import XML_POSITION
from docxray.exceptions import InvalidXmlError
from docxray.lxml import BaseOxmlElement
from docxray.oxml.transitional.ns import nsmap
from docxray.oxml.transitional.simpletypes import SimpleType
from docxray.types import ELM_T

ST_T = TypeVar("ST_T", bound=SimpleType)
T = TypeVar("T")

nsmap_reversed = {v: k for k, v in nsmap.items()}


class OxmlElement(BaseOxmlElement):
    def xpath(self, xpath: str) -> Any:  # type: ignore[override]
        return super().xpath(xpath, nsmap)

    @cached_property
    def is_first(self) -> bool:
        tag = self.xml_tag(self.tag)
        return self.xpath(f"not(preceding-sibling::{tag})")

    @cached_property
    def is_last(self) -> bool:
        tag = self.xml_tag(self.tag)
        return self.xpath(f"not(following-sibling::{tag})")

    @cached_property
    def xml_pos(self) -> XML_POSITION:
        return self.xml_position(self.is_first, self.is_last)

    def xml_tag(self, qn_tag: Any) -> str:
        qn = QName(qn_tag)
        if qn.namespace is None:
            msg = "No namespace provided for word element"
            raise InvalidXmlError(msg)
        return f"{nsmap_reversed[qn.namespace]}:{qn.localname}"

    def xml_position(self, is_first: bool, is_last: bool) -> XML_POSITION:
        if not is_first and not is_last:
            return XML_POSITION.MIDDLE
        if is_first and not is_last:
            return XML_POSITION.START
        if not is_first and is_last:
            return XML_POSITION.END
        return XML_POSITION.ONE_ITEM

    def attr_optional(
        self, elm_qn: str, simple_type: type[ST_T], default: T | None = None
    ) -> Any | T:
        attr = self.get(elm_qn)
        if attr is None:
            return default
        return simple_type.validate(attr)

    def attr_required(self, elm_qn: str, simple_type: type[ST_T]) -> Any:
        attr = self.get(elm_qn)
        if attr is None:
            msg = (
                f"Attribute {elm_qn} was None when one was required for {self}"
            )
            raise InvalidXmlError(msg)
        return simple_type.validate(attr)

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
