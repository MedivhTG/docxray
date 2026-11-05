from __future__ import annotations

from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE_URI
from docxray2.xmlchemy import (
    AttrOptional,
    AttrRequired,
    BaseOxmlElement,
    elm_ns_cls_lookup,
)
from docxray2.xsd.st_primitives import XsdAnyUri, XsdID

from .xsd import ST_ContentType, ST_Extension, ST_TargetMode

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
    Extension = AttrRequired("Extension", ST_Extension)
    ContentType = AttrRequired("ContentType", ST_ContentType)


class CT_Override(OpcOxmlNSMediaTypesStream):
    ContentType = AttrRequired("ContentType", ST_ContentType)
    PartName = AttrRequired("PartName", XsdAnyUri)


class CT_Relationships(OpcOxmlNSRelationships):
    @property
    def relationships(self) -> list[E_Relationship]:
        return self.zero_or_more(E_Relationship)


class CT_Relationship(OpcOxmlNSRelationships):
    TargetMode = AttrOptional("TargetMode", ST_TargetMode)
    Target = AttrRequired("Target", XsdAnyUri)
    Type = AttrRequired("Type", XsdAnyUri)
    Id = AttrRequired("Id", XsdID)


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
