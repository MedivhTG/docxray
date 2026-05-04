from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.shared import CT_DecimalNumber
from docxray.oxml.simpletypes import ST_DecimalNumber
from docxray.oxml.xmlchemy import OxmlElement


class CT_NumPicBullet(OxmlElement):
    pass


class CT_AbstractNum(OxmlElement):
    pass


class CT_Num(OxmlElement):
    @cached_property
    def numId(self) -> int:
        return self.attr_required(W.NUM_ID, ST_DecimalNumber)

    @cached_property
    def abstractNumId(self) -> CT_DecimalNumber:
        return self.child_exactly_one(W.ABSTRACT_NUM_ID, CT_DecimalNumber)


class CT_Numbering(OxmlElement):
    @cached_property
    def numPicBullet_lst(self) -> list[CT_NumPicBullet]:
        return self.child_zero_or_more(W.NUM_PIC_BULLET, CT_NumPicBullet)

    @cached_property
    def abstractNum_lst(self) -> list[CT_AbstractNum]:
        return self.child_zero_or_more(W.ABSTRACT_NUM, CT_AbstractNum)

    @cached_property
    def num_lst(self) -> list[CT_Num]:
        return self.child_zero_or_max(W.NUM, CT_Num, 9)

    @cached_property
    def numIdMacAtCleanup(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(
            W.NUM_ID_MAC_AT_CLEANUP, CT_DecimalNumber
        )
