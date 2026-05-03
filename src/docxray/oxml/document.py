"""Custom element classes that correspond to the document part, e.g. <w:document>."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.table import CT_Tbl
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.xmlchemy import OxmlElement


class CT_Document(OxmlElement):
    """``<w:document>`` element, the root element of a document.xml file."""

    @cached_property
    def body(self) -> CT_Body:
        return self.child_exactly_one(W.BODY, CT_Body)


class CT_Body(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        return self.xpath("w:p | w:tbl")
