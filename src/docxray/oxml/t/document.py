from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.t.background import CT_Background
from docxray.oxml.t.ns import W
from docxray.oxml.t.shared import CT_AltChunk, CT_SectPr
from docxray.oxml.t.table.table import CT_Tbl
from docxray.oxml.t.text.paragraph import CT_P, EG_RunLevelElts
from docxray.oxml.t.xmlchemy import OxmlElement

type EG_ContentBlockContent = CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | EG_RunLevelElts
type EG_BlockLevelChunkElts = EG_ContentBlockContent
type EG_BlockLevelElts = EG_BlockLevelChunkElts | CT_AltChunk

XPATH_BLOCK_LEVEL_ELTS = (
    "w:customXml | w:sdt | w:p | w:tbl | "
    "w:proofErr | w:permStart | w:permEnd | w:bookmarkStart | "
    "w:bookmarkEnd | w:moveFromRangeStart | w:moveFromRangeEnd | "
    "w:moveToRangeStart | w:commentRangeEnd | w:customXmlInsRangeStart | "
    "w:customXmlInsRangeEnd | w:customXmlDelRangeStart | "
    "w:customXmlDelRangeEnd | w:customXmlMoveFromRangeStart | "
    "w:customXmlMoveFromRangeEnd | w:customXmlMoveToRangeStart | "
    "w:customXmlMoveToRangeEnd | w:ins | w:del | w:moveFrom | "
    "w:moveTo | m:oMathPara | m:oMath | CT_AltChunk"
)


class CT_CustomXmlBlock(OxmlElement):
    pass


class CT_SdtBlock(OxmlElement):
    pass


class CT_Body(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[EG_BlockLevelElts]:
        return self.xpath(XPATH_BLOCK_LEVEL_ELTS)

    @cached_property
    def sectPr(self) -> CT_SectPr | None:
        return self.child_zero_or_one(W.SECT_PR, CT_SectPr)


class CT_DocumentBase(OxmlElement):
    @cached_property
    def background(self) -> CT_Background | None:
        return self.child_zero_or_one(W.BACKGROUND, CT_Background)


class CT_Document(CT_DocumentBase):
    @cached_property
    def body(self) -> CT_Body:
        return self.child_exactly_one(W.BODY, CT_Body)
