"""Custom element classes related to the styles part."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.ns import W
from docxray.oxml.xmlchemy import OxmlElement


class CT_Style(OxmlElement):
    """A ``<w:style>`` element, representing a style definition."""

    @cached_property
    def type(self) -> WD_STYLE_TYPE | None:
        return self.get_enum(W.TYPE, WD_STYLE_TYPE)


class CT_Styles(OxmlElement):
    """``<w:styles>`` element, the root element of a styles part, i.e. styles.xml."""

    def get_by_id(self, styleId: str) -> CT_Style | None:
        """`w:style` child where @styleId = `styleId`.

        |None| if not found.
        """
        return self.find(f"{W.STYLE}[@{W.STYLE_ID}='{styleId}']", CT_Style)
