from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import CT_Border, CT_String, CT_TblWidth
from docxray.oxml.trans.st.shared_common import ST_OnOff
from docxray.oxml.trans.st.wml import ST_ShortHexNumber
from docxray.oxml.trans.xmlchemy import OxmlElement


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


class CT_TblPr(OxmlElement):
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
