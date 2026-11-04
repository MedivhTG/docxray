from typing import Self

from lxml import etree

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import BaseOxmlElement, elm_ns_cls_lookup

oxml_nslookup = elm_ns_cls_lookup()
oxml_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
oxml_parser.set_element_class_lookup(oxml_nslookup)


OXML_NSMAP = {
    "w": NAMESPACE.MAIN_DOCUMENT,
    "cp": NAMESPACE.CORE_PROPERTIES,
    "ep": NAMESPACE.EXTENDED_PROPERTIES,
    "xml": NAMESPACE.XML,
}


class Oxml(BaseOxmlElement, nslookup=oxml_nslookup, nsmap=OXML_NSMAP):
    @classmethod
    def from_xml(cls, text: str | bytes) -> Self:
        return cls.parse(text, oxml_parser)
