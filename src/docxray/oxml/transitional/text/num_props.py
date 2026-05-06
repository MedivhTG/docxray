from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.ns import W
from docxray.oxml.transitional.shared import CT_DecimalNumber, CT_TrackChange
from docxray.oxml.transitional.simpletypes import ST_String
from docxray.oxml.transitional.xmlchemy import OxmlElement


class CT_TrackChangeNumbering(CT_TrackChange):
    @cached_property
    def original(self) -> str | None:
        return self.attr_optional(W.ORIGINAL, ST_String)


class CT_NumPr(OxmlElement):
    @cached_property
    def ilvl(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.ILVL, CT_DecimalNumber)

    @cached_property
    def numId(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.NUM_ID, CT_DecimalNumber)

    @cached_property
    def numberingChange(self) -> CT_TrackChangeNumbering | None:
        return self.child_zero_or_one(
            W.NUMBERING_CHANGE, CT_TrackChangeNumbering
        )

    @cached_property
    def ins(self) -> CT_TrackChange | None:
        return self.child_zero_or_one(W.INS, CT_TrackChange)
