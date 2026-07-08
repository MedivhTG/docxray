from functools import cached_property

# docxray stuff
from docxray.oxml.t.ns import W
from docxray.oxml.t.shared import (
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
from docxray.oxml.t.st.enums import (
    SE_LINE_SPACING_RULE,
    SE_TEXT_ALIGNMENT,
    SE_ON_OFF_1,
)
from docxray.oxml.t.st.shared_common import ST_OnOff, ST_TwipsMeasure
from docxray.oxml.t.st.wml import (
    ST_DecimalNumber,
    ST_LineSpacingRule,
    ST_SignedTwipsMeasure,
    ST_TextAlignment,
)
from docxray.oxml.t.xmlchemy import OxmlElement

from .num_props import CT_NumPr
from .run_props import CT_RPr


class CT_PBdr(OxmlElement):
    pass


class CT_Tabs(OxmlElement):
    pass


class CT_Spacing(OxmlElement):
    @cached_property
    def before(self) -> int | str | None:
        return self.attr_optional(W.BEFORE, ST_TwipsMeasure)

    @cached_property
    def beforeLines(self) -> int | None:
        return self.attr_optional(W.BEFORE_LINES, ST_DecimalNumber)

    @cached_property
    def beforeAutospacing(self) -> bool | SE_ON_OFF_1 | None:
        return self.attr_optional(W.BEFORE_AUTOSPACING, ST_OnOff)

    @cached_property
    def after(self) -> int | str | None:
        return self.attr_optional(W.AFTER, ST_TwipsMeasure)

    @cached_property
    def afterLines(self) -> int | None:
        return self.attr_optional(W.AFTER_LINES)

    @cached_property
    def afterAutospacing(self) -> bool | SE_ON_OFF_1 | None:
        return self.attr_optional(W.AFTER_AUTOSPACING, ST_OnOff)

    @cached_property
    def line(self) -> int | str | None:
        return self.attr_optional(W.LINE, ST_SignedTwipsMeasure)

    @cached_property
    def lineRule(self) -> SE_LINE_SPACING_RULE:
        return self.attr_optional(
            W.LINE_RULE, ST_LineSpacingRule, SE_LINE_SPACING_RULE.AUTO
        )


class CT_Ind(OxmlElement):
    @cached_property
    def start(self) -> int | str | None:
        return self.attr_optional(W.START, ST_SignedTwipsMeasure)

    @cached_property
    def startChars(self) -> int | None:
        return self.attr_optional(W.START_CHARS, ST_DecimalNumber)

    @cached_property
    def end(self) -> int | str | None:
        return self.attr_optional(W.END, ST_SignedTwipsMeasure)

    @cached_property
    def endChars(self) -> int | None:
        return self.attr_optional(W.END_CHARS, ST_DecimalNumber)

    @cached_property
    def left(self) -> int | str | None:
        return self.attr_optional(W.LEFT, ST_SignedTwipsMeasure)

    @cached_property
    def leftChars(self) -> int | None:
        return self.attr_optional(W.LEFT_CHARS, ST_DecimalNumber)

    @cached_property
    def right(self) -> int | str | None:
        return self.attr_optional(W.RIGHT, ST_SignedTwipsMeasure)

    @cached_property
    def rightChars(self) -> int | None:
        return self.attr_optional(W.RIGHT_CHARS, ST_DecimalNumber)

    @cached_property
    def hanging(self) -> int | str | None:
        return self.attr_optional(W.HANGING, ST_TwipsMeasure)

    @cached_property
    def hangingChars(self) -> int | None:
        return self.attr_optional(W.HANGING_CHARS, ST_DecimalNumber)

    @cached_property
    def firstLine(self) -> int | str | None:
        return self.attr_optional(W.FIRST_LINE, ST_TwipsMeasure)

    @cached_property
    def firstLineChars(self) -> int | None:
        return self.attr_optional(W.FIRST_LINE_CHARS, ST_DecimalNumber)


class CT_TextAlignment(OxmlElement):
    @cached_property
    def val(self) -> SE_TEXT_ALIGNMENT:
        return self.attr_required(W.VAL, ST_TextAlignment)


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
        return self.child_zero_or_one(W.SPACING, CT_Spacing)

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
