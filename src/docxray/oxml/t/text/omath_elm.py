from functools import cached_property

# docxray stuff
from docxray.oxml.t.ns import XML, M, W
from docxray.oxml.t.shared import CT_OnOff
from docxray.oxml.t.st.enums import (
    SE_F_TYPE,
    SE_LIM_LOC,
    SE_SCRIPT,
    SE_SHP,
    SE_STYLE,
    SE_TOP_BOT,
    SE_X_ALIGN,
    SE_Y_ALIGN,
)
from docxray.oxml.t.st.shared_common import ST_String, ST_XAlign, ST_YAlign
from docxray.oxml.t.st.shared_math import (
    ST_Char,
    ST_FType,
    ST_Integer2,
    ST_Integer255,
    ST_LimLoc,
    ST_Script,
    ST_Shp,
    ST_SpacingRule,
    ST_Style,
    ST_TopBot,
    ST_UnSignedInteger,
)
from docxray.oxml.t.xmlchemy import OxmlElement

from .run import RUN_INNER_CONTENT_XPATH, RunInnerContent
from .run_props import CT_RPr

type OMathElements = CT_Acc | CT_Bar | CT_Box | CT_BorderBox | CT_D | CT_EqArr | CT_F | CT_Func | CT_GroupChr | CT_LimLow | CT_LimUpp | CT_M | CT_Nary | CT_Phant | CT_Rad | CT_SPre | CT_SSub | CT_SSubSup | CT_SSup | CT_R_OMath
OMATH_ELEMENTS_XPATH = "m:acc | m:bar | m:box | m:borderBox | m:d | m:eqArr | m:f | m:func | m:groupChr | m:limLow | m:limUpp | m:m | m:nary | m:phant | m:rad | m:sPre | m:sSub | m:sSubSup | m:sSup | m:r"


class CT_Integer2(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(M.VAL, ST_Integer2)


class CT_Integer255(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(M.VAL, ST_Integer255)


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

    # TODO: look for paragraph content too
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

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


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


class CT_LimLowPr(OxmlElement):
    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_LimUppPr(OxmlElement):
    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_LimLow(OxmlElement):
    @cached_property
    def limLowPr(self) -> CT_LimLowPr | None:
        return self.child_zero_or_one(M.LIM_LOW_PR, CT_LimLowPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)

    @cached_property
    def lim(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.LIM, CT_OMathArg)


class CT_LimUpp(OxmlElement):
    @cached_property
    def limUppPr(self) -> CT_LimUppPr | None:
        return self.child_zero_or_one(M.LIM_UPP_PR, CT_LimUppPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)

    @cached_property
    def lim(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.LIM, CT_OMathArg)


class CT_XAlign(OxmlElement):
    @cached_property
    def val(self) -> SE_X_ALIGN:
        return self.attr_required(M.VAL, ST_XAlign)


class CT_MCPr(OxmlElement):
    @cached_property
    def count(self) -> CT_Integer255 | None:
        return self.child_zero_or_one(M.COUNT, CT_Integer255)

    @cached_property
    def mcJc(self) -> CT_XAlign | None:
        return self.child_zero_or_one(M.MC_JC, CT_XAlign)


class CT_MC(OxmlElement):
    @cached_property
    def mcPr(self) -> CT_MCPr | None:
        return self.child_zero_or_one(M.MC_PR, CT_MCPr)


class CT_MCS(OxmlElement):
    @cached_property
    def mc(self) -> list[CT_MC]:
        return self.child_zero_or_more(M.MC, CT_MC)


class CT_MPr(OxmlElement):
    @cached_property
    def baseJc(self) -> CT_YAlign | None:
        return self.child_zero_or_one(M.BASE_JC, CT_YAlign)

    @cached_property
    def plcHide(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.PLC_HIDE, CT_OnOff)

    @cached_property
    def rSpRule(self) -> CT_SpacingRule | None:
        return self.child_zero_or_one(M.R_SP_RULE, CT_SpacingRule)

    @cached_property
    def cGpRule(self) -> CT_SpacingRule | None:
        return self.child_zero_or_one(M.C_GP_RULE, CT_SpacingRule)

    @cached_property
    def rSp(self) -> CT_UnSignedInteger | None:
        return self.child_zero_or_one(M.R_SP, CT_UnSignedInteger)

    @cached_property
    def cSp(self) -> CT_UnSignedInteger | None:
        return self.child_zero_or_one(M.C_SP, CT_UnSignedInteger)

    @cached_property
    def cGp(self) -> CT_UnSignedInteger | None:
        return self.child_zero_or_one(M.C_GP, CT_UnSignedInteger)

    @cached_property
    def mcs(self) -> CT_MCS | None:
        return self.child_zero_or_one(M.MCS, CT_MCS)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_MR(OxmlElement):
    @cached_property
    def e(self) -> list[CT_OMathArg]:
        return self.child_zero_or_more(M.E, CT_OMathArg)


class CT_M(OxmlElement):
    @cached_property
    def mPr(self) -> CT_MPr | None:
        return self.child_zero_or_one(M.M_PR, CT_MPr)

    @cached_property
    def mr(self) -> list[CT_MR]:
        return self.child_zero_or_more(M.MR, CT_MR)


class CT_LimLoc(OxmlElement):
    @cached_property
    def val(self) -> SE_LIM_LOC:
        return self.attr_required(M.VAL, ST_LimLoc)


class CT_NaryPr(OxmlElement):
    @cached_property
    def chr(self) -> CT_Char | None:
        return self.child_zero_or_one(M.CHR, CT_Char)

    @cached_property
    def limLoc(self) -> CT_LimLoc | None:
        return self.child_zero_or_one(M.LIM_LOC, CT_LimLoc)

    @cached_property
    def grow(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.GROW, CT_OnOff)

    @cached_property
    def subHide(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.SUB_HIDE, CT_OnOff)

    @cached_property
    def supHide(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.SUP_HIDE, CT_OnOff)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Nary(OxmlElement):
    @cached_property
    def naryPr(self) -> CT_NaryPr | None:
        return self.child_zero_or_one(M.NARY_PR, CT_NaryPr)

    @cached_property
    def sub(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUB, CT_OMathArg)

    @cached_property
    def sup(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUP, CT_OMathArg)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_PhantPr(OxmlElement):
    @cached_property
    def show(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.SHOW, CT_OnOff)

    @cached_property
    def zeroWid(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.ZERO_WID, CT_OnOff)

    @cached_property
    def zeroAsc(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.ZERO_ASC, CT_OnOff)

    @cached_property
    def zeroDesc(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.ZERO_DESC, CT_OnOff)

    @cached_property
    def transp(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.TRANSP, CT_OnOff)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Phant(OxmlElement):
    @cached_property
    def phantPr(self) -> CT_PhantPr | None:
        return self.child_zero_or_one(M.PHANT_PR, CT_PhantPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_RadPr(OxmlElement):
    @cached_property
    def degHide(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.DEG_HIDE, CT_OnOff)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_Rad(OxmlElement):
    @cached_property
    def radPr(self) -> CT_RadPr | None:
        return self.child_zero_or_one(M.RAD_PR, CT_RadPr)

    @cached_property
    def deg(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.DEG, CT_OMathArg)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_SPrePr(OxmlElement):
    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_SPre(OxmlElement):
    @cached_property
    def sPrePr(self) -> CT_SPrePr | None:
        return self.child_zero_or_one(M.S_PRE_PR, CT_SPrePr)

    @cached_property
    def sub(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUB, CT_OMathArg)

    @cached_property
    def sup(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUP, CT_OMathArg)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)


class CT_SSubPr(OxmlElement):
    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_SSub(OxmlElement):
    @cached_property
    def sSubPr(self) -> CT_SSubPr | None:
        return self.child_zero_or_one(M.S_SUB_PR, CT_SSubPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)

    @cached_property
    def sub(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUB, CT_OMathArg)


class CT_SSubSupPr(OxmlElement):
    @cached_property
    def alnScr(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.ALN_SCR, CT_OnOff)

    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_SSubSup(OxmlElement):
    @cached_property
    def sSubSupPr(self) -> CT_SSubSupPr | None:
        return self.child_zero_or_one(M.S_SUB_SUP_PR, CT_SSubSupPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)

    @cached_property
    def sub(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUB, CT_OMathArg)

    @cached_property
    def sup(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUP, CT_OMathArg)


class CT_SSupPr(OxmlElement):
    @cached_property
    def ctrlPr(self) -> CT_CtrlPr | None:
        return self.child_zero_or_one(M.CTRL_PR, CT_CtrlPr)


class CT_SSup(OxmlElement):
    @cached_property
    def sSupPr(self) -> CT_SSupPr | None:
        return self.child_zero_or_one(M.S_SUP_PR, CT_SSupPr)

    @cached_property
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)

    @cached_property
    def sup(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.SUP, CT_OMathArg)


class CT_Text_OMath(OxmlElement):
    @cached_property
    def txt(self) -> str:
        return self.text or ""

    @cached_property
    def space(self) -> str | None:
        return self.attr_optional(XML.SPACE, ST_String)


class CT_Script(OxmlElement):
    @cached_property
    def val(self) -> SE_SCRIPT:
        return self.attr_optional(M.VAL, ST_Script)


class CT_Style_OMath(OxmlElement):
    @cached_property
    def val(self) -> SE_STYLE:
        return self.attr_optional(M.VAL, ST_Style)


class CT_RPR(OxmlElement):
    @cached_property
    def lit(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.LIT, CT_OnOff)

    @cached_property
    def brk(self) -> CT_ManualBreak | None:
        return self.child_zero_or_one(M.BRK, CT_ManualBreak)

    @cached_property
    def nor(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.NOR, CT_OnOff)

    @cached_property
    def scr(self) -> CT_Script | None:
        return self.child_zero_or_one(M.SCR, CT_Script)

    @cached_property
    def sty(self) -> CT_Style_OMath | None:
        return self.child_zero_or_one(M.STY, CT_Style_OMath)

    @cached_property
    def aln(self) -> CT_OnOff | None:
        return self.child_zero_or_one(M.ALN, CT_OnOff)


class CT_R_OMath(OxmlElement):
    @cached_property
    def rPr_omath(self) -> CT_RPR | None:
        return self.child_zero_or_one(M.R_PR, CT_RPR)

    @cached_property
    def rPr_run(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def inner_content_items(self) -> list[RunInnerContent | CT_Text_OMath]:
        return self.xpath(f"{RUN_INNER_CONTENT_XPATH} | m:t")
