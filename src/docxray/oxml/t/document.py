from functools import cached_property

# docxray stuff
from docxray.oxml.t.background import CT_Background
from docxray.oxml.t.ns import W
from docxray.oxml.t.shared import CT_AltChunk, CT_SectPr
from docxray.oxml.t.table.table import CT_Tbl
from docxray.oxml.t.text.paragraph import CT_P
from docxray.oxml.t.xmlchemy import OxmlElement


class CT_Body(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        return self.xpath("w:p | w:tbl")

    @cached_property
    def altChunk_lst(self) -> list[CT_AltChunk]:
        return self.child_zero_or_more(W.ALT_CHUNK, CT_AltChunk)

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
