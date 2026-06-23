from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import M, W
from docxray.oxml.trans.st.enums import SE_TOP_BOT
from docxray.oxml.trans.st.shared_math import ST_Char, ST_Integer2, ST_TopBot
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
