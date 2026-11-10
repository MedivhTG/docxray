from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE, NAMESPACE_URI
from docxray2.xmlchemy import (
    AttrRequired,
    BaseOxmlElement,
    elm_ns_cls_lookup,
)

opc_nslookup = elm_ns_cls_lookup()
opc_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
opc_parser.set_element_class_lookup(opc_nslookup)

OPC_NSMAP: dict[str | None, str] = {
    "ct": NAMESPACE_URI.MEDIA_TYPES_STREAM,
    "r": NAMESPACE_URI.RELATIONSHIPS,
    "cp": NAMESPACE.CORE_PROPERTIES,
    "xml": NAMESPACE.XML,
    "xsi": NAMESPACE.XML_SHEMA_INSTANCE,
    "dc": NAMESPACE.DUBLIN_CORE,
    "dcterms": NAMESPACE.DUBLIN_CORE_TERMS,
}


class OpcOxml(
    BaseOxmlElement,
    nslookup=opc_nslookup,
    nsmap=OPC_NSMAP,
):
    @classmethod
    def new(
        cls,
        exclude_tag_prefix: bool = False,
        nsmap: dict[None | str, str] | None = None,
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
            elif cls._namespace in OPC_NSMAP:
                nsmap = {cls._namespace: OPC_NSMAP[cls._namespace]}
            else:
                nsmap = OPC_NSMAP
        return opc_parser.makeelement(
            qname, nsmap=nsmap, attrib=attrib
        )  # type: ignore[return-value]

    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, opc_parser)
