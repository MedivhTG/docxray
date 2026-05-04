"""Custom element classes related to the styles part."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.enum.word import WD_STYLE_TYPE, WD_TBL_STYLE_OVERRIDE_TYPE
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_String
from docxray.oxml.simpletypes import ST_StyleType, ST_TblStyleOverrideType
from docxray.oxml.table.cell_props import CT_TcPr
from docxray.oxml.table.row_props import CT_TrPr
from docxray.oxml.table.table_props import CT_TblPrBase
from docxray.oxml.text.paragraph_props import CT_PPr
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

    @cached_property
    def pPr(self) -> CT_PPr | None:
        return self.child_zero_or_one(W.P_PR, CT_PPr)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def tblPr(self) -> CT_TblPrBase | None:
        return self.child_zero_or_one(W.TBL_PR, CT_TblPrBase)

    @cached_property
    def trPr(self) -> CT_TrPr | None:
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)

    @cached_property
    def tcPr(self) -> CT_TcPr | None:
        return self.child_zero_or_one(W.TC_PR, CT_TcPr)


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
    def tblStylePr_lst(self) -> list[CT_TblStylePr]:
        return self.child_zero_or_more(W.TBL_STYLE_PR, CT_TblStylePr)

    def tblStylePr_for(
        self, type: WD_TBL_STYLE_OVERRIDE_TYPE
    ) -> CT_TblStylePr | None:
        tblStylPr_elm = self.find(
            f"./{W.TBL_STYLE_PR}[@{W.TYPE}='{type}']", CT_TblStylePr
        )
        if tblStylPr_elm is None:
            return None
        return tblStylPr_elm


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
