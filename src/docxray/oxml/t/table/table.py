from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.t.ns import W
from docxray.oxml.t.xmlchemy import OxmlElement

from .cell_props import CT_TcPr
from .row_props import CT_TblPrEx, CT_TrPr
from .table_props import CT_TblPr

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.document import EG_BlockLevelElts


class CT_Tc(OxmlElement):
    @cached_property
    def tcPr(self) -> CT_TcPr | None:
        return self.child_zero_or_one(W.TC_PR, CT_TcPr)

    @cached_property
    def inner_content_elements(self) -> list[EG_BlockLevelElts]:
        # docxray stuff
        from docxray.oxml.t.document import XPATH_BLOCK_LEVEL_ELTS

        return self.xpath(XPATH_BLOCK_LEVEL_ELTS)


class CT_Row(OxmlElement):
    @cached_property
    def trPr(self) -> CT_TrPr | None:
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)

    @cached_property
    def tblPrEx(self) -> CT_TblPrEx | None:
        return self.child_zero_or_one(W.TBL_PR_EX, CT_TblPrEx)

    @cached_property
    def tc_lst(self) -> list[CT_Tc]:
        return self.child_zero_or_more(W.TC, CT_Tc)


class CT_Tbl(OxmlElement):
    @cached_property
    def tblPr(self) -> CT_TblPr:
        return self.child_exactly_one(W.TBL_PR, CT_TblPr)

    @cached_property
    def tr_lst(self) -> list[CT_Row]:
        return self.child_zero_or_more(W.TR, CT_Row)
