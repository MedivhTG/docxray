"""Custom element classes that correspond to the document part, e.g. <w:document>."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.background import CT_Background
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_AltChunk
from docxray.oxml.table import CT_Tbl
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.xmlchemy import OxmlElement


class CT_DocumentBase(OxmlElement):
    @cached_property
    def background(self) -> CT_Background | None:
        return self.child_zero_or_one(W.BACKGROUND, CT_Background)


class CT_Document(CT_DocumentBase):
    """``<w:document>`` element, the root element of a document.xml file."""

    @cached_property
    def body(self) -> CT_Body:
        return self.child_exactly_one(W.BODY, CT_Body)


class CT_SectPr(OxmlElement):
    pass


class CT_Body(OxmlElement):
    # -- Сhoice for EG_BlockLevelElts

    @cached_property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        return self.xpath("w:p | w:tbl")

    @cached_property
    def altChunk_lst(self) -> list[CT_AltChunk]:
        return self.child_zero_or_more(W.ALT_CHUNK, CT_AltChunk)

    # -- EndChoice for EG_BlockLevelElts

    @cached_property
    def sectPr(self) -> CT_SectPr | None:
        return self.child_zero_or_one(W.SECT_PR, CT_SectPr)
