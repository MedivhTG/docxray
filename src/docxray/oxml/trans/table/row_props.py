from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import CT_Cnf
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_TrPr(OxmlElement):
    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)

    # @cached_property
    # def tblCellSpacing(self) -> CT_TblWidth
