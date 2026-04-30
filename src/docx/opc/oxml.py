"""Temporary stand-in for main oxml module.

This module came across with the PackageReader transplant. Probably much will get
replaced with objects from the pptx.oxml.core and then this module will either get
deleted or only hold the package related custom element classes.
"""

from __future__ import annotations

from typing import TypeVar

from lxml import etree

from docx.lxml import BaseOxmlElement, elm_ns_cls_lookup
from docx.opc.constants import RELATIONSHIP_TARGET_MODE as RTM
from docx.opc.exceptions import OpcError
from docx.opc.ns import nsmap, CT, PR

# configure XML parser
lookup = etree.ElementNamespaceClassLookup()
parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
parser.set_element_class_lookup(lookup)


class OpcOxmlElement(BaseOxmlElement):
    def get_one(self, tag: str) -> str:
        attr = self.get(tag)
        if attr is None:
            msg = f"Cannot get '{tag}' from {self}"
            raise OpcError(msg)
        return attr


lookup = elm_ns_cls_lookup(OpcOxmlElement)
parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
parser.set_element_class_lookup(lookup)

ELM_T = TypeVar("ELM_T", bound=OpcOxmlElement)


def parse_xml(
    text: str | bytes, assert_element: type[ELM_T] = OpcOxmlElement
) -> ELM_T:
    elm = etree.fromstring(text, parser)
    assert isinstance(elm, assert_element)
    return elm


class CT_Default(OpcOxmlElement):
    """`<Default>` element that appears in `[Content_Types].xml` part.

    Used to specify a default content type to be applied to any part with the specified extension.
    """

    @property
    def content_type(self):
        """String held in the ``ContentType`` attribute of this ``<Default>``
        element."""
        return self.get_one("ContentType")

    @property
    def extension(self):
        """String held in the ``Extension`` attribute of this ``<Default>`` element."""
        return self.get_one("Extension")


class CT_Override(OpcOxmlElement):
    """``<Override>`` element, specifying the content type to be applied for a part with
    the specified partname."""

    @property
    def content_type(self):
        """String held in the ``ContentType`` attribute of this ``<Override>``
        element."""
        return self.get_one("ContentType")

    @property
    def partname(self):
        """String held in the ``PartName`` attribute of this ``<Override>`` element."""
        return self.get_one("PartName")


class CT_Relationship(OpcOxmlElement):
    """`<Relationship>` element, representing a single relationship from source to target part."""

    @property
    def rId(self) -> str:
        """String held in the ``Id`` attribute of this ``<Relationship>`` element."""
        return self.get_one("Id")

    @property
    def reltype(self) -> str:
        """String held in the ``Type`` attribute of this ``<Relationship>`` element."""
        return self.get_one("Type")

    @property
    def target_ref(self) -> str:
        """String held in the ``Target`` attribute of this ``<Relationship>``
        element."""
        return self.get_one("Target")

    @property
    def target_mode(self) -> str:
        """String held in the ``TargetMode`` attribute of this ``<Relationship>``
        element, either ``Internal`` or ``External``.

        Defaults to ``Internal``.
        """
        return self.get("TargetMode", RTM.INTERNAL)


class CT_Relationships(OpcOxmlElement):
    """``<Relationships>`` element, the root element in a .rels file."""

    @property
    def Relationship_lst(self) -> list[CT_Relationship]:
        """Return a list containing all the ``<Relationship>`` child elements."""
        return self.findall(PR.RELATIONSHIP, CT_Relationship)


class CT_Types(OpcOxmlElement):
    """``<Types>`` element, the container element for Default and Override elements in
    [Content_Types].xml."""

    @property
    def defaults(self):
        return self.findall(CT.DEFAULT, CT_Default)

    @property
    def overrides(self):
        return self.findall(CT.OVERRIDE, CT_Override)


ct_namespace = lookup.get_namespace(nsmap["ct"])
ct_namespace["Default"] = CT_Default
ct_namespace["Override"] = CT_Override
ct_namespace["Types"] = CT_Types

pr_namespace = lookup.get_namespace(nsmap["pr"])
pr_namespace["Relationship"] = CT_Relationship
pr_namespace["Relationships"] = CT_Relationships
