from functools import cached_property

# docxray stuff
from docxray.enum.word import WD_MULTILEVEL_TYPE
from docxray.oxml.ns import W
from docxray.oxml.shared import (
    CT_DecimalNumber,
    CT_Jc,
    CT_LongHexNumber,
    CT_OnOff,
    CT_String,
)
from docxray.oxml.simpletypes import (
    ST_DecimalNumber,
    ST_LongHexNumber,
    ST_MultiLevelType,
    ST_OnOff,
)
from docxray.oxml.text.paragraph_props import CT_PPr
from docxray.oxml.text.run_props import CT_RPr
from docxray.oxml.xmlchemy import OxmlElement


class CT_NumPicBullet(OxmlElement):
    pass


class CT_NumFmt(OxmlElement):
    pass


class CT_LevelSuffix(OxmlElement):
    pass


class CT_LevelText(OxmlElement):
    pass


class CT_LvlLegacy(OxmlElement):
    pass


class CT_Lvl(OxmlElement):
    @cached_property
    def ilvl(self) -> int:
        return self.attr_required(W.ILVL, ST_DecimalNumber)

    @cached_property
    def tplc(self) -> int | None:
        return self.attr_optional(W.TPLC, ST_LongHexNumber)

    @cached_property
    def tentaive(self) -> bool | None:
        return self.attr_optional(W.TENTAIVE, ST_OnOff)

    @cached_property
    def start(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.START, CT_DecimalNumber)

    @cached_property
    def numFmt(self) -> CT_NumFmt | None:
        return self.child_zero_or_one(W.NUM_FMT, CT_NumFmt)

    @cached_property
    def lvlRestart(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.LVL_RESTART, CT_DecimalNumber)

    @cached_property
    def pStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.P_STYLE, CT_String)

    @cached_property
    def isLgl(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.IS_LGL, CT_OnOff)

    @cached_property
    def suff(self) -> CT_LevelSuffix | None:
        return self.child_zero_or_one(W.SUFF, CT_LevelSuffix)

    @cached_property
    def lvlText(self) -> CT_LevelText | None:
        return self.child_zero_or_one(W.LVL_TEXT, CT_LevelText)

    @cached_property
    def lvlPicBulletId(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.LVL_PIC_BULLET_ID, CT_DecimalNumber)

    @cached_property
    def legacy(self) -> CT_LvlLegacy | None:
        return self.child_zero_or_one(W.LEGACY, CT_LvlLegacy)

    @cached_property
    def lvlJc(self) -> CT_Jc | None:
        return self.child_zero_or_one(W.LVL_JC, CT_Jc)

    @cached_property
    def pPr(self) -> CT_PPr | None:
        return self.child_zero_or_one(W.P_PR, CT_PPr)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)


class CT_MultiLevelType(OxmlElement):
    @cached_property
    def val(self) -> WD_MULTILEVEL_TYPE:
        return self.attr_required(W.VAL, ST_MultiLevelType)


class CT_AbstractNum(OxmlElement):
    @cached_property
    def abstractNumId(self) -> int:
        return self.attr_required(W.ABSTRACT_NUM_ID, ST_DecimalNumber)

    @cached_property
    def nsid(self) -> CT_LongHexNumber | None:
        return self.child_zero_or_one(W.NSID, CT_LongHexNumber)

    @cached_property
    def multiLevelType(self) -> CT_MultiLevelType | None:
        return self.child_zero_or_one(W.MULTI_LEVEL_TYPE, CT_MultiLevelType)

    @cached_property
    def tmpl(self) -> CT_LongHexNumber | None:
        return self.child_zero_or_one(W.TMPL, CT_LongHexNumber)

    @cached_property
    def name(self) -> CT_String | None:
        return self.child_zero_or_one(W.NAME, CT_String)

    @cached_property
    def styleLink(self) -> CT_String | None:
        return self.child_zero_or_one(W.STYLE_LINK, CT_String)

    @cached_property
    def numStyleLink(self) -> CT_String | None:
        return self.child_zero_or_one(W.NUM_STYLE_LINK, CT_String)

    @cached_property
    def lvl_lst(self) -> list[CT_Lvl]:
        return self.child_zero_or_n(W.LVL, CT_Lvl, 9)

    def lvl_by_ilvl(self, ilvl_val: int) -> CT_Lvl | None:
        return self.child_zero_or_one(
            f"./{W.LVL}[@{W.ILVL}='{ilvl_val}']", CT_Lvl
        )

    def lvl_by_pStyle(self, pStyle_val: str) -> CT_Lvl | None:
        lvl_elms: list[CT_Lvl] = self.xpath(
            f"./w:lvl[w:pStyle[@w:val='{pStyle_val}']]"
        )
        if lvl_elms:
            return lvl_elms[0]
        return None


class CT_NumLvl(OxmlElement):
    @cached_property
    def ilvl(self) -> int:
        return self.attr_required(W.ILVL, ST_DecimalNumber)

    @cached_property
    def startOverride(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.START_OVERRIDE, CT_DecimalNumber)

    @cached_property
    def lvl(self) -> CT_Lvl | None:
        return self.child_zero_or_one(W.LVL, CT_Lvl)


class CT_Num(OxmlElement):
    @cached_property
    def numId(self) -> int:
        return self.attr_required(W.NUM_ID, ST_DecimalNumber)

    @cached_property
    def abstractNumId(self) -> CT_DecimalNumber:
        return self.child_exactly_one(W.ABSTRACT_NUM_ID, CT_DecimalNumber)

    @cached_property
    def lvlOverride_lst(self) -> list[CT_NumLvl]:
        return self.child_zero_or_n(W.LVL_OVERRIDE, CT_NumLvl, 9)

    def override_num_by_ilvl(self, ilvl_val: int) -> CT_NumLvl | None:
        return self.child_zero_or_one(
            f"./{W.LVL_OVERRIDE}[@{W.ILVL}='{ilvl_val}']", CT_NumLvl
        )


class CT_Numbering(OxmlElement):
    @cached_property
    def numPicBullet_lst(self) -> list[CT_NumPicBullet]:
        return self.child_zero_or_more(W.NUM_PIC_BULLET, CT_NumPicBullet)

    @cached_property
    def abstractNum_lst(self) -> list[CT_AbstractNum]:
        return self.child_zero_or_more(W.ABSTRACT_NUM, CT_AbstractNum)

    @cached_property
    def num_lst(self) -> list[CT_Num]:
        return self.child_zero_or_more(W.NUM, CT_Num)

    @cached_property
    def numIdMacAtCleanup(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(
            W.NUM_ID_MAC_AT_CLEANUP, CT_DecimalNumber
        )

    def num_by_id(self, numId_val: int) -> CT_Num | None:
        return self.child_zero_or_one(
            f"./{W.NUM}[@{W.NUM_ID}='{numId_val}']", CT_Num
        )

    def abstract_num_by_id(
        self, abstract_num_id_val: int
    ) -> CT_AbstractNum | None:
        return self.child_zero_or_one(
            f"./{W.ABSTRACT_NUM}[@{W.ABSTRACT_NUM_ID}='{abstract_num_id_val}']",
            CT_AbstractNum,
        )
