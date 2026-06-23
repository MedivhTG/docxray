from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import M, W
from docxray.oxml.trans.shared import CT_OnOff
from docxray.oxml.trans.st.enums import SE_SHP, SE_TOP_BOT
from docxray.oxml.trans.st.shared_math import (
    ST_Char,
    ST_Integer2,
    ST_Integer255,
    ST_Shp,
    ST_TopBot,
)
from docxray.oxml.trans.xmlchemy import OxmlElement

from .run_props import CT_RPr


class CT_Integer2(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(M.VAL, ST_Integer2)


class CT_OMathArgPr(OxmlElement):
    @cached_property
    def argSz(self) -> CT_Integer2 | None:
        return self.child_zero_or_one(M.ARG_SZ, CT_Integer2)


class CT_OMathArg(OxmlElement):
    @cached_property
    def argPr(self) -> CT_OMathArgPr | None:
        return self.child_zero_or_one(M.ARG_PR, CT_OMathArgPr)


class CT_CtrlPr(OxmlElement):
    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)


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
    def e(self) -> CT_OMathArg | None:
        return self.child_zero_or_one(M.E, CT_OMathArg)
