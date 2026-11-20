from typing import Self

from lxml import etree

# docxray stuff
from docxray2.xmlchemy import (
    Attrib,
    BaseOxmlElement,
    Nsmap,
    NsmapMode,
    elm_ns_cls_lookup,
)

opc_nslookup = elm_ns_cls_lookup()
opc_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
opc_parser.set_element_class_lookup(opc_nslookup)


class OpcOxml(BaseOxmlElement, nslookup=opc_nslookup):
    @classmethod
    def new(
        cls,
        *children: BaseOxmlElement,
        nsmap_override: Nsmap | None = None,
        nsmap_mode: NsmapMode = "single_ns",
        attrib_update: Attrib | None = None,
    ) -> Self:
        return cls.new_element(  # type: ignore[type-var]
            *children,
            parser=opc_parser,  # pyright: ignore[reportArgumentType]
            nsmap_override=nsmap_override,
            nsmap_mode=nsmap_mode,
            attrib_update=attrib_update,
        )

    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, opc_parser)
