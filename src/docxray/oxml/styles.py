"""Custom element classes related to the styles part."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.ns import W
from docxray.oxml.text.run_props import CT_RPr
from docxray.oxml.xmlchemy import OxmlElement


class CT_RPrDefault(OxmlElement):
    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_first(W.R_PR, CT_RPr)


class CT_DocDefaults(OxmlElement):
    @cached_property
    def rPrDefault(self) -> CT_RPrDefault | None:
        return self.child_zero_or_first(W.R_PR_DEFAULT, CT_RPrDefault)


class CT_BasedOn(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.get_attr_one(W.VAL)


class CT_Style(OxmlElement):
    """A ``<w:style>`` element, representing a style definition."""

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_first(W.R_PR, CT_RPr)

    @cached_property
    def type(self) -> WD_STYLE_TYPE | None:
        return self.get_attr_enum(W.TYPE, WD_STYLE_TYPE)

    @cached_property
    def basedOn(self) -> CT_BasedOn | None:
        return self.child_zero_or_first(W.BASED_ON, CT_BasedOn)


class CT_Styles(OxmlElement):
    """``<w:styles>`` element, the root element of a styles part, i.e. styles.xml."""

    @cached_property
    def docDefaults(self) -> CT_DocDefaults | None:
        return self.child_zero_or_first(W.DOC_DEFAULTS, CT_DocDefaults)

    def get_by_id(self, styleId: str) -> CT_Style | None:
        """`w:style` child where @styleId = `styleId`.

        |None| if not found.
        """
        return self.find(f"{W.STYLE}[@{W.STYLE_ID}='{styleId}']", CT_Style)
