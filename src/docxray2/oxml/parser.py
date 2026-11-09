from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import (
    AttrRequired,
    BaseOxmlElement,
    elm_ns_cls_lookup,
)

oxml_nslookup = elm_ns_cls_lookup()
oxml_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
oxml_parser.set_element_class_lookup(oxml_nslookup)


OXML_NSMAP: dict[str | None, str] = {
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
    def new(
        cls,
        exclude_tag_prefix: bool = False,
        nsmap: dict[str | None, str] | None = None,
    ) -> Self:
        attrib = {}
        for attr in cls.attrs().values():
            if isinstance(attr, AttrRequired):
                attrib[attr.qname] = attr.fixed or ""
        qname = cls.qname()
        if nsmap is None:
            uri = qname.namespace
            if exclude_tag_prefix and uri:
                nsmap = {None: uri}
            elif cls._namespace in OXML_NSMAP:
                nsmap = {cls._namespace: OXML_NSMAP[cls._namespace]}
            else:
                nsmap = OXML_NSMAP
        return oxml_parser.makeelement(
            qname, nsmap=nsmap, attrib=attrib
        )  # type: ignore[return-value]

    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, oxml_parser)
