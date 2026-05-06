"""Provides StylesPart and related objects."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.part import TransitionalPart
from docxray.oxml.transitional.proxy.styles.styles import Styles
from docxray.oxml.transitional.styles import CT_Styles


class StylesPart(TransitionalPart[CT_Styles]):
    """Proxy for the styles.xml part containing style definitions for a document or
    glossary."""

    @cached_property
    def styles(self) -> Styles:
        """The |_Styles| instance containing the styles (<w:style> element proxies) for
        this styles part."""
        return Styles(self.element, self)
