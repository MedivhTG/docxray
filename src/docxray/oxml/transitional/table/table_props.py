from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.ns import W
from docxray.oxml.transitional.shared import CT_String
from docxray.oxml.transitional.xmlchemy import OxmlElement


class CT_TblPrBase(OxmlElement):
    @cached_property
    def tblStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.TBL_STYLE, CT_String)


class CT_TblPr(CT_TblPrBase):
    pass
