from __future__ import annotations

from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import (
    Attrib,
    BaseOxmlElement,
    NsmapMode,
    elm_ns_cls_lookup,
)

oxml_nslookup = elm_ns_cls_lookup()
oxml_parser: etree.XMLParser = etree.XMLParser(
    remove_blank_text=True, resolve_entities=False
)
oxml_parser.set_element_class_lookup(oxml_nslookup)


OXML_NSMAP: dict[str | None, str] = {
    "w": NAMESPACE.MAIN_DOCUMENT,
    "ep": NAMESPACE.EXTENDED_PROPERTIES,
    "vt": NAMESPACE.VARIANT_TYPES,
}


class Oxml(
    BaseOxmlElement,
    nslookup=oxml_nslookup,
    nsmap=OXML_NSMAP,
):
    @classmethod
    def new(
        cls,
        *children: BaseOxmlElement,
        nsmap_override: dict[str | None, str] | None = None,
        nsmap_mode: NsmapMode = "single_ns",
        attrib_update: Attrib | None = None,
    ) -> Self:
        nsmap = OXML_NSMAP if nsmap_override is None else nsmap_override
        return cls.new_element(  # type: ignore[type-var]
            *children,
            parser=oxml_parser,  # pyright: ignore[reportArgumentType]
            nsmap=nsmap,
            nsmap_mode=nsmap_mode,
            attrib_update=attrib_update,
        )

    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, oxml_parser)
