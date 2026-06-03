from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import CT_Cnf, CT_Shd, CT_String, CT_TblWidth
from docxray.oxml.trans.st.enums import SE_HEIGHT_RULE
from docxray.oxml.trans.st.shared_common import ST_TwipsMeasure
from docxray.oxml.trans.st.wml import ST_HeightRule
from docxray.oxml.trans.xmlchemy import OxmlElement

from .table_props import (
    CT_JcTable,
    CT_TblBorders,
    CT_TblCellMar,
    CT_TblLayoutType,
    CT_TblLook,
)


class CT_Height(OxmlElement):
    @cached_property
    def val(self) -> int | str | None:
        return self.attr_optional(W.VAL, ST_TwipsMeasure)

    @cached_property
    def hRule(self) -> SE_HEIGHT_RULE | None:
        return self.attr_optional(W.H_RULE, ST_HeightRule)


class CT_TrPr(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)

    @cached_property
    def tblCellSpacing(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_CELL_SPACING, CT_TblWidth)

    @cached_property
    def trHeight(self) -> CT_Height | None:
        return self.child_zero_or_one(W.TR_HEIGHT, CT_Height)


class CT_TblPrEx(OxmlElement):
    @cached_property
    def tblW(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_W, CT_TblWidth)

    @cached_property
    def jc(self) -> CT_JcTable | None:
        return self.child_zero_or_one(W.JC, CT_JcTable)

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
