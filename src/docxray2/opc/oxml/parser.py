from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE, NAMESPACE_URI
from docxray2.xmlchemy import (
    Attrib,
    BaseOxmlElement,
    NsmapMode,
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
        *children: BaseOxmlElement,
        nsmap_override: dict[str | None, str] | None = None,
        nsmap_mode: NsmapMode = "single_ns",
        attrib_update: Attrib | None = None,
    ) -> Self:
        nsmap = OPC_NSMAP if nsmap_override is None else nsmap_override
        return cls.new_element(  # type: ignore[type-var]
            *children,
            parser=opc_parser,  # pyright: ignore[reportArgumentType]
            nsmap=nsmap,
            nsmap_mode=nsmap_mode,
            attrib_update=attrib_update,
        )

    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, opc_parser)
