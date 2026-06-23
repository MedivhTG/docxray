from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import M, W
from docxray.oxml.trans.shared import CT_OnOff
from docxray.oxml.trans.st.enums import (
    SE_F_TYPE,
    SE_SHP,
    SE_TOP_BOT,
    SE_Y_ALIGN,
)
from docxray.oxml.trans.st.shared_common import ST_YAlign
from docxray.oxml.trans.st.shared_math import (
    ST_Char,
    ST_FType,
    ST_Integer2,
    ST_Integer255,
    ST_Shp,
    ST_SpacingRule,
    ST_TopBot,
    ST_UnSignedInteger,
)
from docxray.oxml.trans.xmlchemy import OxmlElement

from .run_props import CT_RPr

type OMathElements = CT_Acc | CT_Bar | CT_Box | CT_BorderBox | CT_D | CT_EqArr | CT_F | CT_Func | CT_GroupChr
OMATH_ELEMENTS_XPATH = "m:acc | m:bar | m:box | m:borderBox | m:d | m:eqArr | m:f | m:func | m:groupChr"


class CT_Integer2(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(M.VAL, ST_Integer2)


class CT_OMathArgPr(OxmlElement):
    @cached_property
    def argSz(self) -> CT_Integer2 | None:
        return self.child_zero_or_one(M.ARG_SZ, CT_Integer2)


class CT_CtrlPr(OxmlElement):
    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)


class CT_OMathArg(OxmlElement):
    @cached_property
    def argPr(self) -> CT_OMathArgPr | None:
        return self.child_zero_or_one(M.ARG_PR, CT_OMathArgPr)

    @cached_property
    def inner_content_items(self) -> list[OMathElements]:
        return self.xpath(OMATH_ELEMENTS_XPATH)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Char(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.attr_required(M.VAL, ST_Char)


class CT_AccPr(OxmlElement):
    @cached_property
    def chr(self) -> CT_Char | None:
        return self.child_zero_or_one(M.CHR, CT_Char)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Acc(OxmlElement):
    @cached_property
    def accPr(self) -> CT_AccPr | None:
        return self.child_zero_or_one(M.ACC_PR, CT_AccPr)


class CT_TopBot(OxmlElement):
    @cached_property
    def val(self) -> SE_TOP_BOT:
        return self.attr_required(M.VAL, ST_TopBot)


class CT_BarPr(OxmlElement):
    @cached_property
    def pos(self) -> CT_TopBot | None:
        return self.child_zero_or_one(M.POS, CT_TopBot)


class CT_Bar(OxmlElement):
    @cached_property
    def barPr(self) -> CT_BarPr | None:
        return self.child_zero_or_one(M.BAR_PR, CT_BarPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_ManualBreak(OxmlElement):
    @cached_property
    def alnAt(self) -> int | None:
        return self.attr_optional(M.ALN_AT, ST_Integer255)


class CT_BoxPr(OxmlElement):
    @cached_property
    def opEmu(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.OP_EMU, CT_OnOff)

    @cached_property
    def noBreak(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.NO_BREAK, CT_OnOff)

    @cached_property
    def diff(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.DIFF, CT_OnOff)

    @cached_property
    def brk(self) -> CT_ManualBreak | None:
        return self.child_zero_or_one(M.BRK, CT_ManualBreak)

    @cached_property
    def aln(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.ALN, CT_OnOff)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Box(OxmlElement):
    @cached_property
    def boxPr(self) -> CT_BoxPr | None:
        return self.child_zero_or_one(M.BOX_PR, CT_BoxPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_BorderBoxPr(OxmlElement):
    @cached_property
    def hideTop(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.HIDE_TOP, CT_OnOff)

    @cached_property
    def hideBot(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.HIDE_BOT, CT_OnOff)

    @cached_property
    def hideLeft(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.HIDE_LEFT, CT_OnOff)

    @cached_property
    def hideRight(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.HIDE_RIGHT, CT_OnOff)

    @cached_property
    def strikeH(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.STRIKE_H, CT_OnOff)

    @cached_property
    def strikeV(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.STRIKE_V, CT_OnOff)

    @cached_property
    def strikeBLTR(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.STRIKE_BLTR, CT_OnOff)

    @cached_property
    def strikeTLBR(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.STRIKE_TLBR, CT_OnOff)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_BorderBox(OxmlElement):
    @cached_property
    def borderBoxPr(self) -> CT_BorderBoxPr | None:
        return self.child_zero_or_one(M.BORDER_BOX_PR, CT_BorderBoxPr)


class CT_Shp(OxmlElement):
    @cached_property
    def val(self) -> SE_SHP:
        return self.attr_required(M.VAL, ST_Shp)


class CT_DPr(OxmlElement):
    @cached_property
    def begChr(self) -> CT_Char | None:
        return self.child_zero_or_one(M.BEG_CHR, CT_Char)

    @cached_property
    def sepChr(self) -> CT_Char | None:
        return self.child_zero_or_one(M.SEP_CHR, CT_Char)

    @cached_property
    def endChr(self) -> CT_Char | None:
        return self.child_zero_or_one(M.END_CHR, CT_Char)

    @cached_property
    def grow(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.GROW, CT_OnOff)

    @cached_property
    def shp(self) -> CT_Shp | None:
        return self.child_zero_or_one(M.SHP, CT_Shp)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_D(OxmlElement):
    @cached_property
    def dPr(self) -> CT_DPr | None:
        return self.child_zero_or_one(M.D_PR, CT_DPr)

    @cached_property
    def e(self) -> list[CT_OMathArg]:
        return self.child_zero_or_more(M.E, CT_OMathArg)


class CT_YAlign(OxmlElement):
    @cached_property
    def val(self) -> SE_Y_ALIGN:
        return self.attr_required(M.VAL, ST_YAlign)


class CT_SpacingRule(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(M.VAL, ST_SpacingRule)


class CT_UnSignedInteger(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(M.VAL, ST_UnSignedInteger)


class CT_EqArrPr(OxmlElement):
    @cached_property
    def baseJc(self) -> CT_YAlign | None:
        return self.child_zero_or_one(M.BASE_JC, CT_YAlign)

    @cached_property
    def maxDist(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.MAX_DIST, CT_OnOff)

    @cached_property
    def objDist(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.OBJ_DIST, CT_OnOff)

    @cached_property
    def rSpRule(self) -> CT_SpacingRule | None:
        return self.child_zero_or_one(M.R_SP_RULE, CT_SpacingRule)

    @cached_property
    def rSp(self) -> CT_UnSignedInteger | None:
        return self.child_zero_or_one(M.R_SP, CT_UnSignedInteger)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_EqArr(OxmlElement):
    @cached_property
    def eqArrPr(self) -> CT_EqArrPr | None:
        return self.child_zero_or_one(M.EQ_ARR_PR, CT_EqArrPr)

    @cached_property
    def e(self) -> list[CT_OMathArg]:
        return self.child_zero_or_more(M.E, CT_OMathArg)


class CT_FType(OxmlElement):
    @cached_property
    def val(self) -> SE_F_TYPE:
        return self.attr_required(M.VAL, ST_FType)


class CT_FPr(OxmlElement):
    @cached_property
    def type(self) -> CT_FType | None:
        return self.child_zero_or_one(M.TYPE, CT_FType)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_F(OxmlElement):
    @cached_property
    def fPr(self) -> CT_FPr | None:
        return self.child_zero_or_one(M.F_PR, CT_FPr)

    @cached_property
    def num(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.NUM, CT_OMathArg)

    @cached_property
    def den(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.DEN, CT_OMathArg)


class CT_FuncPr(OxmlElement):
    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Func(OxmlElement):
    @cached_property
    def funcPr(self) -> CT_FuncPr | None:
        return self.child_zero_or_one(M.FUNC_PR, CT_FuncPr)

    @cached_property
    def fName(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.F_NAME, CT_OMathArg)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_GroupChrPr(OxmlElement):
    @cached_property
    def chr(self) -> CT_Char | None:
        return self.child_zero_or_one(M.CHR, CT_Char)

    @cached_property
    def pos(self) -> CT_TopBot | None:
        return self.child_zero_or_one(M.POS, CT_TopBot)

    @cached_property
    def vertJc(self) -> CT_TopBot | None:
        return self.child_zero_or_one(M.VERT_JC, CT_TopBot)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_GroupChr(OxmlElement):
    @cached_property
    def groupChrPr(self) -> CT_GroupChrPr | None:
        return self.child_zero_or_one(M.GROUP_CHR_PR, CT_GroupChrPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)
