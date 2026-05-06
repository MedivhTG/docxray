"""Provides StylesPart and related objects."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.opc.part import XmlPart
from docxray.oxml.transitional.styles import CT_Styles
from docxray.proxy.styles.styles import Styles


class StylesPart(XmlPart[CT_Styles]):
    """Proxy for the styles.xml part containing style definitions for a document or
    glossary."""

    @cached_property
    def styles(self) -> Styles:
        """The |_Styles| instance containing the styles (<w:style> element proxies) for
        this styles part."""
        return Styles(self.element, self)
