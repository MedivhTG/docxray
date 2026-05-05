from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_AltChunk
from docxray.oxml.table.cell_props import CT_TcPr
from docxray.oxml.table.row_props import CT_TrPr
from docxray.oxml.table.table_props import CT_TblPr
from docxray.oxml.xmlchemy import OxmlElement

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.text.paragraph import CT_P


class CT_Tc(OxmlElement):
    # -- Сhoice for EG_BlockLevelElts

    @cached_property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        return self.xpath("w:p | w:tbl")

    @cached_property
    def altChunk_lst(self) -> list[CT_AltChunk]:
        return self.child_zero_or_more(W.ALT_CHUNK, CT_AltChunk)

    # -- EndChoice for EG_BlockLevelElts

    @cached_property
    def tcPr(self) -> CT_TcPr | None:
        return self.child_zero_or_one(W.TC_PR, CT_TcPr)


class CT_Row(OxmlElement):
    @cached_property
    def trPr(self) -> CT_TrPr | None:
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)

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
