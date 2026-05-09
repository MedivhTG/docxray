from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import (
    CT_Border,
    CT_Cnf,
    CT_DecimalNumber,
    CT_OnOff,
    CT_Shd,
    CT_TblWidth,
    CT_TextDirection,
)
from docxray.oxml.trans.st.enums import SE_Merge
from docxray.oxml.trans.st.wml import ST_Merge
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_HMerge(OxmlElement):
    pass


class CT_VMerge(OxmlElement):
    @cached_property
    def val(self) -> SE_Merge | None:
        return self.attr_optional(W.VAL, ST_Merge)


class CT_TcBorders(OxmlElement):
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


class CT_TcMar(OxmlElement):
    pass


class CT_VerticalJc(OxmlElement):
    pass


class CT_TcPr(OxmlElement):
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
