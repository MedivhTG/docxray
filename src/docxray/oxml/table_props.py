from functools import cached_property

# docxray stuff
from docxray.enum.table import WD_CNF_FORMAT
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_String
from docxray.oxml.simpletypes import ST_Cnf
from docxray.oxml.xmlchemy import OxmlElement


class CT_Cnf(OxmlElement):
    @cached_property
    def val(self) -> WD_CNF_FORMAT:
        return self.attr_required(W.VAL, ST_Cnf)


class CT_TcPr(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)


class CT_TrPr(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)


class CT_TblPrBase(OxmlElement):
    @cached_property
    def tblStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.TBL_STYLE, CT_String)


class CT_TblPr(CT_TblPrBase):
    pass
