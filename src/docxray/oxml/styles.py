"""Custom element classes related to the styles part."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE, WD_TBL_STYLE_OVERRIDE_TYPE
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_String
from docxray.oxml.simpletypes import ST_StyleType, ST_TblStyleOverrideType
from docxray.oxml.text.run_props import CT_RPr
from docxray.oxml.xmlchemy import OxmlElement


class CT_RPrDefault(OxmlElement):
    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)


class CT_DocDefaults(OxmlElement):
    @cached_property
    def rPrDefault(self) -> CT_RPrDefault | None:
        return self.child_zero_or_one(W.R_PR_DEFAULT, CT_RPrDefault)


class CT_TblStylePr(OxmlElement):
    @cached_property
    def type(self) -> WD_TBL_STYLE_OVERRIDE_TYPE:
        return self.attr_required(W.TYPE, ST_TblStyleOverrideType)


class CT_Style(OxmlElement):
    """A ``<w:style>`` element, representing a style definition."""

    @cached_property
    def type(self) -> WD_STYLE_TYPE:
        return self.attr_optional(
            W.TYPE, ST_StyleType, WD_STYLE_TYPE.PARAGRAPH
        )

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def basedOn(self) -> CT_String | None:
        return self.child_zero_or_one(W.BASED_ON, CT_String)

    @cached_property
    def tblStylePr(self) -> list[CT_TblStylePr]:
        return self.child_zero_or_more(W.TBL_STYLE_PR, CT_TblStylePr)


class CT_Styles(OxmlElement):
    """``<w:styles>`` element, the root element of a styles part, i.e. styles.xml."""

    @cached_property
    def docDefaults(self) -> CT_DocDefaults | None:
        return self.child_zero_or_one(W.DOC_DEFAULTS, CT_DocDefaults)

    def get_by_id(self, styleId: str) -> CT_Style | None:
        """`w:style` child where @styleId = `styleId`.

        |None| if not found.
        """
        return self.find(f"{W.STYLE}[@{W.STYLE_ID}='{styleId}']", CT_Style)
