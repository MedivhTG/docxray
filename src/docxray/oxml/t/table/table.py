from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.t.ns import W
from docxray.oxml.t.st.wml import ST_LongHexNumber
from docxray.oxml.t.text.paragraph import (
    _XPATH_RANGE_MARKUP,
    _XPATH_RUN_LEVEL_ELTS,
    EG_RangeMarkupElements,
    EG_RunLevelElts,
)
from docxray.oxml.t.xmlchemy import OxmlElement

from .cell_props import CT_TcPr
from .row_props import CT_TblPrEx, CT_TrPr
from .table_props import CT_TblPr

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.document import EG_BlockLevelElts


type EG_ContentCellContent = CT_Tc | CT_CustomXmlCell | CT_SdtCell | EG_RunLevelElts
type EG_ContentRowContent = CT_Row | CT_CustomXmlRow | CT_SdtRow | EG_RunLevelElts


XPATH_ROW_CONTENT = f"w:tr | w:customXml | w:sdt | {_XPATH_RUN_LEVEL_ELTS}"
XPATH_CELL_CONTENT = f"w:tc | w:customXml | w:sdt | {_XPATH_RUN_LEVEL_ELTS}"


class CT_CustomXmlRow(OxmlElement):
    pass


class CT_SdtRow(OxmlElement):
    pass


class CT_CustomXmlCell(OxmlElement):
    pass


class CT_SdtCell(OxmlElement):
    pass


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
    def tblPrEx(self) -> CT_TblPrEx | None:
        return self.child_zero_or_one(W.TBL_PR_EX, CT_TblPrEx)

    @cached_property
    def trPr(self) -> CT_TrPr | None:
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)

    @cached_property
    def inner_content_elements(self) -> list[EG_ContentCellContent]:
        elms: list[EG_ContentCellContent] = self.xpath(XPATH_CELL_CONTENT)
        elms_recr: list[EG_ContentCellContent] = []
        for elm in elms:
            if elm.tag_name == "customXml":
                elms_recr.append(elm.recreate(CT_CustomXmlCell))
            elif elm.tag_name == "sdt":
                elms_recr.append(elm.recreate(CT_SdtCell))
            else:
                elms_recr.append(elm)
        return elms_recr

    @cached_property
    def rsidRPr(self) -> bytes | None:
        return self.attr_optional(W.RSID_R_PR, ST_LongHexNumber)

    @cached_property
    def rsidR(self) -> bytes | None:
        return self.attr_optional(W.RSID_R, ST_LongHexNumber)

    @cached_property
    def rsidDel(self) -> bytes | None:
        return self.attr_optional(W.RSID_DEL, ST_LongHexNumber)

    @cached_property
    def rsidTr(self) -> bytes | None:
        return self.attr_optional(W.RSID_TR, ST_LongHexNumber)


class CT_TblGrid(OxmlElement):
    pass


class CT_Tbl(OxmlElement):
    @cached_property
    def inner_range_elements(self) -> list[EG_RangeMarkupElements]:
        return self.xpath(_XPATH_RANGE_MARKUP)

    @cached_property
    def tblPr(self) -> CT_TblPr:
        return self.child_exactly_one(W.TBL_PR, CT_TblPr)

    @cached_property
    def tblGrid(self) -> CT_TblGrid:
        return self.child_exactly_one(W.TBL_GRID, CT_TblGrid)

    @cached_property
    def inner_content_items(self) -> list[EG_ContentRowContent]:
        elms: list[EG_ContentRowContent] = self.xpath(XPATH_ROW_CONTENT)
        elms_recr: list[EG_ContentRowContent] = []
        for elm in elms:
            if elm.tag_name == "customXml":
                elms_recr.append(elm.recreate(CT_CustomXmlRow))
            elif elm.tag_name == "sdt":
                elms_recr.append(elm.recreate(CT_SdtRow))
            else:
                elms_recr.append(elm)
        return elms_recr
