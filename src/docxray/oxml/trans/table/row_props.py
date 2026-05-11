from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import CT_Cnf, CT_String, CT_TblWidth
from docxray.oxml.trans.table.table_props import CT_TblBorders, CT_TblLook
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_TrPr(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)

    @cached_property
    def tblCellSpacing(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_CELL_SPACING, CT_TblWidth)


class CT_TblPrEx(OxmlElement):
    @cached_property
    def tblStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.TBL_STYLE, CT_String)

    @cached_property
    def tblBorders(self) -> CT_TblBorders | None:
        return self.child_zero_or_one(W.TBL_BORDERS, CT_TblBorders)

    @cached_property
    def tblCellSpacing(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TBL_CELL_SPACING, CT_TblWidth)

    @cached_property
    def tblLook(self) -> CT_TblLook | None:
        return self.child_zero_or_one(W.TBL_LOOK, CT_TblLook)
