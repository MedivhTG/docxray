# pyright: reportImportCycles=false

"""XML parser for python-docx."""

from __future__ import annotations

from lxml import etree

# docxray stuff
from docxray.lxml import elm_ns_cls_lookup
from docxray.oxml.transitional.ns import nsmap
from docxray.oxml.transitional.xmlchemy import OxmlElement
from docxray.proxy.types import ELM_T

# -- configure XML parser --
lookup = elm_ns_cls_lookup(OxmlElement)
parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
parser.set_element_class_lookup(lookup)


def parse_xml(xml: str | bytes, elm_hint: type[ELM_T]) -> ELM_T:
    """Root lxml element obtained by parsing XML character string `xml`.

    The custom parser is used, so custom element classes are produced for elements in
    `xml` that have them.
    """
    elm = etree.fromstring(xml, parser)
    return elm  # type: ignore[return-value]


def register_element_cls(tag: str, cls: type[OxmlElement]) -> None:
    """Register an lxml custom element-class to use for `tag`.

    A instance of `cls` to be constructed when the oxml parser encounters an element
    with matching `tag`. `tag` is a string of the form `nspfx:tagroot`, e.g.
    `'w:document'`.
    """
    nspfx, tagroot = tag.split(":")
    namespace = lookup.get_namespace(nsmap[nspfx])
    namespace[tagroot] = cls
