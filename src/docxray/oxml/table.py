from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.table_props import CT_TblPr, CT_TcPr, CT_TrPr
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.xmlchemy import OxmlElement


class CT_Tbl(OxmlElement):
    @cached_property
    def tblPr(self) -> CT_TblPr:
        return self.child_exactly_one(W.TBL_PR, CT_TblPr)


class CT_Row(OxmlElement):
    @cached_property
    def trPr(self) -> CT_TrPr | None:
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)


class CT_Tc(OxmlElement):
    @cached_property
    def tcPr(self) -> CT_TcPr | None:
        return self.child_zero_or_one(W.TC_PR, CT_TcPr)

    @cached_property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        return self.xpath("w:p | w:tbl")
