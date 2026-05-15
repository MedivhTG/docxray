"""Provides StylesPart and related objects."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.part import TransitionalPart
from docxray.oxml.trans.proxy.numbering.numbering import Numbering
from docxray.oxml.trans.proxy.styles.styles import Styles
from docxray.oxml.trans.styles import CT_Styles


class StylesPart(TransitionalPart[CT_Styles]):
    """Proxy for the styles.xml part containing style definitions for a document or
    glossary."""

    @cached_property
    def styles(self) -> Styles:
        """The |_Styles| instance containing the styles (<w:style> element proxies) for
        this styles part."""
        return Styles(self.element, self)

    @cached_property
    def numbering(self) -> Numbering | None:
        package = self.package
        assert package is not None
        return package.main_document_part.numbering
