"""Custom element classes that correspond to the document part, e.g. <w:document>."""

from __future__ import annotations

from docx.oxml.xmlchemy import OxmlElement


class CT_Document(OxmlElement):
    """``<w:document>`` element, the root element of a document.xml file."""

    pass
