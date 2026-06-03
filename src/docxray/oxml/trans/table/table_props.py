from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import (
    CT_Border,
    CT_DecimalNumber,
    CT_OnOff,
    CT_Shd,
    CT_String,
    CT_TblWidth,
)
from docxray.oxml.trans.st.enums import SE_JC_TABLE
from docxray.oxml.trans.st.shared_common import ST_OnOff
from docxray.oxml.trans.st.wml import ST_JcTable, ST_ShortHexNumber
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_JcTable(OxmlElement):
    @cached_property
    def val(self) -> SE_JC_TABLE:
        return self.attr_required(W.VAL, ST_JcTable)


class CT_TblLayoutType(OxmlElement):
    pass


class CT_TblCellMar(OxmlElement):
    @cached_property
    def top(self) -> CT_TblWidth | None:
        top_elm = self.child_zero_or_one(W.TOP, CT_TblWidth)
        if top_elm is None:
            return None
        return top_elm.recreate(CT_TblWidth)

    @cached_property
    def start(self) -> CT_TblWidth | None:
        start_elm = self.child_zero_or_one(W.START, CT_TblWidth)
        if start_elm is None:
            return None
        return start_elm.recreate(CT_TblWidth)

    @cached_property
    def left(self) -> CT_TblWidth | None:
        left_elm = self.child_zero_or_one(W.LEFT, CT_TblWidth)
        if left_elm is None:
            return None
        return left_elm.recreate(CT_TblWidth)

    @cached_property
    def bottom(self) -> CT_TblWidth | None:
        bottom_elm = self.child_zero_or_one(W.BOTTOM, CT_TblWidth)
        if bottom_elm is None:
            return None
        return bottom_elm.recreate(CT_TblWidth)

    @cached_property
    def end(self) -> CT_TblWidth | None:
        end_elm = self.child_zero_or_one(W.END, CT_TblWidth)
        if end_elm is None:
            return None
        return end_elm.recreate(CT_TblWidth)

    @cached_property
    def right(self) -> CT_TblWidth | None:
        right_elm = self.child_zero_or_one(W.RIGHT, CT_TblWidth)
        if right_elm is None:
            return None
        return right_elm.recreate(CT_TblWidth)


class CT_TblLook(OxmlElement):
    @cached_property
    def val(self) -> bytes | None:
        return self.attr_optional(W.VAL, ST_ShortHexNumber)

    @cached_property
    def firstRow(self) -> bool | None:
        return self.attr_optional(W.FIRST_ROW, ST_OnOff)

    @cached_property
    def lastRow(self) -> bool | None:
        return self.attr_optional(W.LAST_ROW, ST_OnOff)

    @cached_property
    def firstColumn(self) -> bool | None:
        return self.attr_optional(W.FIRST_COLUMN, ST_OnOff)

    @cached_property
    def lastColumn(self) -> bool | None:
        return self.attr_optional(W.LAST_COLUMN, ST_OnOff)

    @cached_property
    def noHBand(self) -> bool | None:
        return self.attr_optional(W.NO_H_BAND, ST_OnOff)

    @cached_property
    def noVBand(self) -> bool | None:
        return self.attr_optional(W.NO_V_BAND, ST_OnOff)


class CT_TblBorders(OxmlElement):
    @cached_property
    def top(self) -> CT_Border | None:
        return self.child_zero_or_one(W.TOP, CT_Border)

    @cached_property
    def left(self) -> CT_Border | None:
        return self.child_zero_or_one(W.LEFT, CT_Border)

    @cached_property
    def bottom(self) -> CT_Border | None:
        return self.child_zero_or_one(W.BOTTOM, CT_Border)

    @cached_property
    def right(self) -> CT_Border | None:
        return self.child_zero_or_one(W.RIGHT, CT_Border)

    @cached_property
    def insideH(self) -> CT_Border | None:
        return self.child_zero_or_one(W.INSIDE_H, CT_Border)

    @cached_property
    def insideV(self) -> CT_Border | None:
        return self.child_zero_or_one(W.INSIDE_V, CT_Border)

    @cached_property
    def tl2br(self) -> CT_Border | None:
        return self.child_zero_or_one(W.TL_2_BR, CT_Border)

    @cached_property
    def tr2bl(self) -> CT_Border | None:
        return self.child_zero_or_one(W.TR_2_BL, CT_Border)


class CT_TblPPr(OxmlElement):
    pass


class CT_TblOverlap(OxmlElement):
    pass


class CT_TblPr(OxmlElement):
    @cached_property
    def tblStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.TBL_STYLE, CT_String)

    @cached_property
    def tblpPr(self) -> CT_TblPPr | None:
        return self.child_zero_or_one(W.TBLP_PR, CT_TblPPr)

    @cached_property
    def tblOverlap(self) -> CT_TblOverlap | None:
        return self.child_zero_or_one(W.TBL_OVERLAP, CT_TblOverlap)

    @cached_property
    def bidiVisual(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.BIDI_VISUAL, CT_OnOff)

    @cached_property
    def tblStyleRowBandSize(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(
            W.TBL_STYLE_ROW_BAND_SIZE, CT_DecimalNumber
        )

    @cached_property
    def tblStyleColBandSize(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(
            W.TBL_STYLE_COL_BAND_SIZE, CT_DecimalNumber
        )

    @cached_property
    def tblW(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_W, CT_TblWidth)

    @cached_property
    def jc(self) -> CT_JcTable | None:
        jc_elm = self.child_zero_or_one(W.JC, CT_JcTable)
        if jc_elm is None:
            return None
        return jc_elm.recreate(CT_JcTable)

    @cached_property
    def tblCellSpacing(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_CELL_SPACING, CT_TblWidth)

    @cached_property
    def tblInd(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_IND, CT_TblWidth)

    @cached_property
    def tblBorders(self) -> CT_TblBorders | None:
        return self.child_zero_or_one(W.TBL_BORDERS, CT_TblBorders)

    @cached_property
    def shd(self) -> CT_Shd | None:
        return self.child_zero_or_one(W.SHD, CT_Shd)

    @cached_property
    def tblLayout(self) -> CT_TblLayoutType | None:
        return self.child_zero_or_one(W.TBL_LAYOUT, CT_TblLayoutType)

    @cached_property
    def tblCellMar(self) -> CT_TblCellMar | None:
        return self.child_zero_or_one(W.TBL_CELL_MAR, CT_TblCellMar)

    @cached_property
    def tblLook(self) -> CT_TblLook | None:
        return self.child_zero_or_one(W.TBL_LOOK, CT_TblLook)

    @cached_property
    def tblCaption(self) -> CT_String | None:
        return self.child_zero_or_one(W.TBL_CAPTION, CT_String)

    @cached_property
    def tblDescription(self) -> CT_String | None:
        return self.child_zero_or_one(W.TBL_DESCRIPTION, CT_String)
