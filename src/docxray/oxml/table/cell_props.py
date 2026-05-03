from functools import cached_property

# docxray stuff
from docxray.enum.table import WD_MERGE
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_Cnf, CT_DecimalNumber, CT_OnOff
from docxray.oxml.simpletypes import ST_Merge
from docxray.oxml.xmlchemy import OxmlElement


class CT_TblWidth(OxmlElement):
    pass


class CT_HMerge(OxmlElement):
    pass


class CT_VMerge(OxmlElement):
    @cached_property
    def val(self) -> WD_MERGE:
        return self.attr_optional(W.VAL, ST_Merge, WD_MERGE.CONTINUE)


class CT_TcBorders(OxmlElement):
    pass


class CT_Shd(OxmlElement):
    pass


class CT_TcMar(OxmlElement):
    pass


class CT_TextDirection(OxmlElement):
    pass


class CT_VerticalJc(OxmlElement):
    pass


class CT_TcPrBase(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)

    @cached_property
    def tcW(self) -> CT_TblWidth | None:
        return self.child_zero_or_one(W.TC_W, CT_TblWidth)

    @cached_property
    def gridSpan(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.GRID_SPAN, CT_DecimalNumber)

    @cached_property
    def hMerge(self) -> CT_HMerge | None:
        return self.child_zero_or_one(W.H_MERGE, CT_HMerge)

    @cached_property
    def vMerge(self) -> CT_VMerge | None:
        return self.child_zero_or_one(W.V_MERGE, CT_VMerge)

    @cached_property
    def tcBorders(self) -> CT_TcBorders | None:
        return self.child_zero_or_one(W.TC_BORDERS, CT_TcBorders)

    @cached_property
    def shd(self) -> CT_Shd | None:
        return self.child_zero_or_one(W.SHD, CT_Shd)

    @cached_property
    def noWrap(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.NO_WRAP, CT_OnOff)

    @cached_property
    def tcMar(self) -> CT_TcMar | None:
        return self.child_zero_or_one(W.TC_MAR, CT_TcMar)

    @cached_property
    def textDirection(self) -> CT_TextDirection | None:
        return self.child_zero_or_one(W.TEXT_DIRECTION, CT_TextDirection)

    @cached_property
    def tcFitText(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.TC_FIT_TEXT, CT_OnOff)

    @cached_property
    def vAlign(self) -> CT_VerticalJc | None:
        return self.child_zero_or_one(W.V_ALIGN, CT_VerticalJc)

    @cached_property
    def hideMark(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.HIDE_MARK, CT_OnOff)


class CT_TcPrInner(CT_TcPrBase):
    pass


class CT_TcPr(CT_TcPrInner):
    pass
