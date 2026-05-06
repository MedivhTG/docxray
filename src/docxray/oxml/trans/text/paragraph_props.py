from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import (
    CT_Cnf,
    CT_DecimalNumber,
    CT_FramePr,
    CT_Jc,
    CT_OnOff,
    CT_SectPr,
    CT_Shd,
    CT_String,
    CT_TextDirection,
    CT_TrackChange,
)
from docxray.oxml.trans.text.num_props import CT_NumPr
from docxray.oxml.trans.text.run_props import CT_RPr
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_PBdr(OxmlElement):
    pass


class CT_Tabs(OxmlElement):
    pass


class CT_Spacing(OxmlElement):
    pass


class CT_Ind(OxmlElement):
    pass


class CT_TextAlignment(OxmlElement):
    pass


class CT_TextboxTightWrap(OxmlElement):
    pass


class CT_ParaRPrOriginal(OxmlElement):
    pass


class CT_ParaRPrChange(CT_TrackChange):
    @cached_property
    def rPr(self) -> CT_ParaRPrOriginal:
        return CT_ParaRPrOriginal(self.child_exactly_one(W.R_PR, CT_RPr))


class CT_ParaRPr(OxmlElement):
    pass


class CT_PPr(OxmlElement):
    @cached_property
    def pStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.P_STYLE, CT_String)

    @cached_property
    def keepNext(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.KEEP_NEXT, CT_OnOff)

    @cached_property
    def keepLines(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.KEEP_LINES, CT_OnOff)

    @cached_property
    def pageBreakBefore(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.PAGE_BREAK_BEFORE, CT_OnOff)

    @cached_property
    def framePr(self) -> CT_FramePr | None:
        return self.child_zero_or_one(W.FRAME_PR, CT_FramePr)

    @cached_property
    def widowControl(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.WIDOW_CONTROL, CT_OnOff)

    @cached_property
    def numPr(self) -> CT_NumPr | None:
        return self.child_zero_or_one(W.NUM_PR, CT_NumPr)

    @cached_property
    def suppressLineNumbers(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SUPPRESS_LINE_NUMBERS, CT_OnOff)

    @cached_property
    def pBdr(self) -> CT_PBdr | None:
        return self.child_zero_or_one(W.P_BDR, CT_PBdr)

    @cached_property
    def shd(self) -> CT_Shd | None:
        return self.child_zero_or_one(W.SHD, CT_Shd)

    @cached_property
    def tabs(self) -> CT_Tabs | None:
        return self.child_zero_or_one(W.TABS, CT_Tabs)

    @cached_property
    def suppressAutoHyphens(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SUPPRESS_AUTO_HYPHENS, CT_OnOff)

    @cached_property
    def kinsoku(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.KINSOKU, CT_OnOff)

    @cached_property
    def wordWrap(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.WORD_WRAP, CT_OnOff)

    @cached_property
    def overflowPunct(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.OVERFLOW_PUNCT, CT_OnOff)

    @cached_property
    def topLinePunct(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.TOP_LINE_PUNCT, CT_OnOff)

    @cached_property
    def autoSpaceDE(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.AUTO_SPACE_DE, CT_OnOff)

    @cached_property
    def autoSpaceDN(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.AUTO_SPACE_DN, CT_OnOff)

    @cached_property
    def bidi(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.BIDI, CT_OnOff)

    @cached_property
    def adjustRightInd(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.ADJUST_RIGHT_IND, CT_OnOff)

    @cached_property
    def snapToGrid(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SNAP_TO_GRID, CT_OnOff)

    @cached_property
    def spacing(self) -> CT_Spacing | None:
        spacing_elm = self.child_zero_or_one(W.SPACING, OxmlElement)
        if spacing_elm is None:
            return None
        return CT_Spacing(spacing_elm)

    @cached_property
    def ind(self) -> CT_Ind | None:
        return self.child_zero_or_one(W.IND, CT_Ind)

    @cached_property
    def contextualSpacing(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.CONTEXTUAL_SPACING, CT_OnOff)

    @cached_property
    def mirrorIndents(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.MIRROR_INDENTS, CT_OnOff)

    @cached_property
    def suppressOverlap(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SUPPRESS_OVERLAP, CT_OnOff)

    @cached_property
    def jc(self) -> CT_Jc | None:
        return self.child_zero_or_one(W.JC, CT_Jc)

    @cached_property
    def textDirection(self) -> CT_TextDirection | None:
        return self.child_zero_or_one(W.TEXT_DIRECTION, CT_TextDirection)

    @cached_property
    def textAlignment(self) -> CT_TextAlignment | None:
        return self.child_zero_or_one(W.TEXT_ALIGNMENT, CT_TextAlignment)

    @cached_property
    def textboxTightWrap(self) -> CT_TextboxTightWrap | None:
        return self.child_zero_or_one(
            W.TEXTBOX_TIGHT_WRAP, CT_TextboxTightWrap
        )

    @cached_property
    def outlineLvl(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.OUTLINE_LVL, CT_DecimalNumber)

    @cached_property
    def divId(self) -> CT_DecimalNumber | None:
        return self.child_zero_or_one(W.DIV_ID, CT_DecimalNumber)

    @cached_property
    def cnfStyle(self) -> CT_Cnf | None:
        return self.child_zero_or_one(W.CNF_STYLE, CT_Cnf)

    @cached_property
    def rPr(self) -> CT_ParaRPr | None:
        rPr = self.child_zero_or_one(W.R_PR, CT_RPr)
        if rPr is None:
            return None
        return CT_ParaRPr(rPr)

    @cached_property
    def sectPr(self) -> CT_SectPr | None:
        return self.child_zero_or_one(W.SECT_PR, CT_SectPr)


class CT_PPrChange(CT_TrackChange):
    @cached_property
    def pPr(self) -> CT_PPr:
        return self.child_exactly_one(W.P_PR, CT_PPr)
