from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.enum.word import WD_UNDERLINE, WD_VERTICAL_ALIGN_RUN
from docxray.oxml.ns import W
from docxray.oxml.shared import (
    CT_Border,
    CT_Color,
    CT_EastAsianLayout,
    CT_Em,
    CT_FitText,
    CT_Fonts,
    CT_Highlight,
    CT_HpsMeasure,
    CT_Language,
    CT_OnOff,
    CT_Shd,
    CT_SignedHpsMeasure,
    CT_SignedTwipsMeasure,
    CT_String,
    CT_TextEffect,
    CT_TextScale,
    CT_TrackChange,
)
from docxray.oxml.simpletypes import ST_Underline, ST_VerticalAlignRun
from docxray.oxml.xmlchemy import OxmlElement


class CT_VerticalAlignRun(OxmlElement):
    @cached_property
    def val(self) -> WD_VERTICAL_ALIGN_RUN:
        return self.attr_required(W.VAL, ST_VerticalAlignRun)


class CT_Underline(OxmlElement):
    @cached_property
    def val(self) -> WD_UNDERLINE:
        return self.attr_optional(W.VAL, ST_Underline, WD_UNDERLINE.SINGLE)


class CT_RPr(OxmlElement):
    @cached_property
    def rStyle(self) -> CT_String | None:
        return self.child_zero_or_one(W.R_STYLE, CT_String)

    @cached_property
    def rFonts(self) -> CT_Fonts | None:
        return self.child_zero_or_one(W.R_FONTS, CT_Fonts)

    @cached_property
    def b(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.B, CT_OnOff)

    @cached_property
    def bCs(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.B_CS, CT_OnOff)

    @cached_property
    def i(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.I, CT_OnOff)

    @cached_property
    def iCs(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.I_CS, CT_OnOff)

    @cached_property
    def caps(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.CAPS, CT_OnOff)

    @cached_property
    def smallCaps(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SMALL_CAPS, CT_OnOff)

    @cached_property
    def strike(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.STRIKE, CT_OnOff)

    @cached_property
    def dstrike(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.DSTRIKE, CT_OnOff)

    @cached_property
    def outline(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.OUTLINE, CT_OnOff)

    @cached_property
    def shadow(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SHADOW, CT_OnOff)

    @cached_property
    def emboss(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.EMBOSS, CT_OnOff)

    @cached_property
    def imprint(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.IMPRINT, CT_OnOff)

    @cached_property
    def noProof(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.NO_PROOF, CT_OnOff)

    @cached_property
    def snapToGrid(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SNAP_TO_GRID, CT_OnOff)

    @cached_property
    def vanish(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.VANISH, CT_OnOff)

    @cached_property
    def webHidden(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.WEB_HIDDEN, CT_OnOff)

    @cached_property
    def color(self) -> CT_Color | None:
        return self.child_zero_or_one(W.COLOR, CT_Color)

    @cached_property
    def spacing(self) -> CT_SignedTwipsMeasure | None:
        return self.child_zero_or_one(W.SPACING, CT_SignedTwipsMeasure)

    @cached_property
    def w(self) -> CT_TextScale | None:
        return self.child_zero_or_one(W.W, CT_TextScale)

    @cached_property
    def kern(self) -> CT_HpsMeasure | None:
        return self.child_zero_or_one(W.KERN, CT_HpsMeasure)

    @cached_property
    def position(self) -> CT_SignedHpsMeasure | None:
        return self.child_zero_or_one(W.POSITION, CT_SignedHpsMeasure)

    @cached_property
    def sz(self) -> CT_HpsMeasure | None:
        return self.child_zero_or_one(W.SZ, CT_HpsMeasure)

    @cached_property
    def szCs(self) -> CT_HpsMeasure | None:
        return self.child_zero_or_one(W.SZ_CS, CT_HpsMeasure)

    @cached_property
    def highlight(self) -> CT_Highlight | None:
        return self.child_zero_or_one(W.HIGHLIGHT, CT_Highlight)

    @cached_property
    def u(self) -> CT_Underline | None:
        return self.child_zero_or_one(W.U, CT_Underline)

    @cached_property
    def effect(self) -> CT_TextEffect | None:
        return self.child_zero_or_one(W.EFFECT, CT_TextEffect)

    @cached_property
    def bdr(self) -> CT_Border | None:
        return self.child_zero_or_one(W.BDR, CT_Border)

    @cached_property
    def shd(self) -> CT_Shd | None:
        return self.child_zero_or_one(W.SHD, CT_Shd)

    @cached_property
    def fitText(self) -> CT_FitText | None:
        return self.child_zero_or_one(W.FIT_TEXT, CT_FitText)

    @cached_property
    def vertAlign(self) -> CT_VerticalAlignRun | None:
        return self.child_zero_or_one(W.VERT_ALIGN, CT_VerticalAlignRun)

    @cached_property
    def rtl(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.RTL, CT_OnOff)

    @cached_property
    def cs(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.CS, CT_OnOff)

    @cached_property
    def em(self) -> CT_Em | None:
        return self.child_zero_or_one(W.EM, CT_Em)

    @cached_property
    def lang(self) -> CT_Language | None:
        return self.child_zero_or_one(W.LANG, CT_Language)

    @cached_property
    def eastAsianLayout(self) -> CT_EastAsianLayout | None:
        return self.child_zero_or_one(W.EAST_ASIAN_LAYOUT, CT_EastAsianLayout)

    @cached_property
    def specVanish(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.SPEC_VANISH, CT_OnOff)

    @cached_property
    def oMath(self) -> CT_OnOff | None:
        return self.child_zero_or_one(W.O_MATH, CT_OnOff)

    @cached_property
    def rPrChange(self) -> CT_RPrChange | None:
        return self.child_zero_or_one(W.R_PR_CHANGE, CT_RPrChange)


class CT_RPrChange(CT_TrackChange):
    @cached_property
    def rPr(self) -> CT_RPr:
        return self.child_exactly_one(W.R_PR, CT_RPr)
