"""Custom element classes that correspond to the document part, e.g. <w:document>."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.xmlchemy import OxmlElement


class CT_Document(OxmlElement):
    """``<w:document>`` element, the root element of a document.xml file."""

    @cached_property
    def body(self) -> CT_Body:
        return self.child_one(W.BODY, CT_Body)


class CT_Body(OxmlElement):
    pass
