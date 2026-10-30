from __future__ import annotations

from typing import Self

from lxml import etree

from ..ns import NAMESPACE_URI
from ..xmlchemy import (
    AttrRequired,
    BaseOxmlElement,
    elm_ns_cls_lookup,
)
from ..xsd.st_primitives import XsdAnyUri, XsdID
from .xsd import ST_ContentType, ST_Extension

opc_nslookup = elm_ns_cls_lookup()
opc_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
opc_parser.set_element_class_lookup(opc_nslookup)

OPC_NSMAP = {
    "ct": NAMESPACE_URI.MEDIA_TYPES_STREAM,
    "r": NAMESPACE_URI.RELATIONSHIPS,
}


class OpcOxml(BaseOxmlElement, nslookup=opc_nslookup, nsmap=OPC_NSMAP):
    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, opc_parser)


class OpcOxmlNSMediaTypesStream(OpcOxml, ns="ct"):
    pass


class OpcOxmlNSRelationships(OpcOxml, ns="r"):
    pass


class CT_Types(OpcOxmlNSMediaTypesStream):
    @property
    def defaults(self) -> list[E_Default]:
        return self.zero_or_more(E_Default)

    @property
    def overrides(self) -> list[E_Override]:
        return self.zero_or_more(E_Override)


class CT_Default(OpcOxmlNSMediaTypesStream):
    extension = AttrRequired("Extension", ST_Extension)
    content_type = AttrRequired("ContentType", ST_ContentType)


class CT_Override(OpcOxmlNSMediaTypesStream):
    content_type = AttrRequired("ContentType", ST_ContentType)
    part_name = AttrRequired("PartName", XsdAnyUri)


class CT_Relationships(OpcOxmlNSRelationships):
    @property
    def relationships(self) -> list[E_Relationship]:
        return self.zero_or_more(E_Relationship)


class CT_Relationship(OpcOxmlNSRelationships):
    target_part = AttrRequired("Target", XsdAnyUri)
    rel_type = AttrRequired("Type", XsdAnyUri)
    rel_id = AttrRequired("Id", XsdID)


# Registration
class E_Types(CT_Types, tag="Types"):
    pass


class E_Default(CT_Default, tag="Default"):
    pass


class E_Override(CT_Override, tag="Override"):
    pass


class E_Relationships(CT_Relationships, tag="Relationships"):
    pass


class E_Relationship(CT_Relationship, tag="Relationship"):
    pass
