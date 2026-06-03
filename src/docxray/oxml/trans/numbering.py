from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import (
    CT_DecimalNumber,
    CT_Jc,
    CT_LongHexNumber,
    CT_OnOff,
    CT_String,
)
from docxray.oxml.trans.st.enums import (
    SE_LEVEL_SUFFIX,
    SE_NUMBER_FORMAT,
    SE_MultilevelType,
    SE_OnOff1,
)
from docxray.oxml.trans.st.shared_common import ST_OnOff, ST_String
from docxray.oxml.trans.st.wml import (
    ST_DecimalNumber,
    ST_LevelSuffix,
    ST_LongHexNumber,
    ST_MultiLevelType,
    ST_NumberFormat,
)
from docxray.oxml.trans.text.paragraph_props import CT_PPr
from docxray.oxml.trans.text.run_props import CT_RPr
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_NumPicBullet(OxmlElement):
    pass


class CT_NumFmt(OxmlElement):
    @cached_property
    def val(self) -> SE_NUMBER_FORMAT:
        return self.attr_required(W.VAL, ST_NumberFormat)

    @cached_property
    def format(self) -> str | None:
        return self.attr_optional(W.FORMAT, ST_String)


class CT_LevelSuffix(OxmlElement):
    @cached_property
    def val(self) -> SE_LEVEL_SUFFIX:
        return self.attr_required(W.VAL, ST_LevelSuffix)


class CT_LevelText(OxmlElement):
    @cached_property
    def val(self) -> str | None:
        return self.attr_optional(W.VAL, ST_String)

    @cached_property
    def null(self) -> bool | SE_OnOff1 | None:
        return self.attr_optional(W.NULL, ST_OnOff)


class CT_LvlLegacy(OxmlElement):
    pass


class CT_Lvl(OxmlElement):
    @cached_property
    def ilvl(self) -> int:
        return self.attr_required(W.ILVL, ST_DecimalNumber)

    @cached_property
    def tplc(self) -> bytes | None:
        return self.attr_optional(W.TPLC, ST_LongHexNumber)

    @cached_property
    def tentative(self) -> bool | None:
        return self.attr_optional(W.TENTATIVE, ST_OnOff)

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
    def val(self) -> SE_MultilevelType:
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
        lvl_elms = self.xpath(f"./w:lvl[@w:ilvl='{ilvl_val}']")
        if len(lvl_elms) > 0:
            return lvl_elms[0]
        return None

    def lvl_by_para_style(self, style_id: str) -> CT_Lvl | None:
        lvl_elms: list[CT_Lvl] = self.xpath(
            f"./w:lvl[w:pStyle[@w:val='{style_id}']]"
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

    def override_num_by_ilvl(self, ilvl: int) -> CT_NumLvl | None:
        numLvl_elms = self.xpath(f"./w:lvlOverride[@w:ilvl='{ilvl}']")
        if len(numLvl_elms) > 0:
            return numLvl_elms[0]
        return None


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

    def num_by_id(self, id: int) -> CT_Num | None:
        num_elms = self.xpath(f"./w:num[@w:numId='{id}']")
        if len(num_elms) > 0:
            return num_elms[0]
        return None

    def abstract_num_by_id(self, id: int) -> CT_AbstractNum | None:
        abstractNum_elms = self.xpath(
            f"./w:abstractNum[@w:abstractNumId='{id}']"
        )
        if len(abstractNum_elms) > 0:
            return abstractNum_elms[0]
        return None
