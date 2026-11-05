from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import (
    AttrRequired,
    BaseOxmlElement,
    ElementAttrsRegistry,
    elm_ns_cls_lookup,
)

oxml_nslookup = elm_ns_cls_lookup()
oxml_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
oxml_parser.set_element_class_lookup(oxml_nslookup)


OXML_NSMAP = {
    "w": NAMESPACE.MAIN_DOCUMENT,
    "cp": NAMESPACE.CORE_PROPERTIES,
    "ep": NAMESPACE.EXTENDED_PROPERTIES,
    "xml": NAMESPACE.XML,
    "xsi": NAMESPACE.XML_SHEMA_INSTANCE,
    "dc": NAMESPACE.DUBLIN_CORE,
    "dcterms": NAMESPACE.DUBLIN_CORE_TERMS,
}


class Oxml(
    BaseOxmlElement,
    nslookup=oxml_nslookup,
    nsmap=OXML_NSMAP,
):
    @classmethod
    def new(cls, exclude_namespace: bool = False) -> Self:
        attrib = {}
        for attr in cls.attrs().values():
            if isinstance(attr, AttrRequired):
                attrib[attr.qname] = attr.fixed or ""
        qname = cls.qname()
        if exclude_namespace:
            tagname = qname.localname
        else:
            tagname = qname
        return oxml_parser.makeelement(
            tagname, nsmap=OXML_NSMAP, attrib=attrib
        )  # pyright: ignore[reportReturnType]

    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, oxml_parser)
