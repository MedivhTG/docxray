from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import A, NoNS
from docxray.oxml.trans.st.dml_main import (
    ST_Angle,
    ST_FixedPercentage,
    ST_Percentage,
    ST_PositiveFixedAngle,
    ST_PositiveFixedPercentage,
    ST_PositivePercentage,
    ST_PresetColorVal,
    ST_SchemeColorVal,
    ST_SystemColorVal,
)
from docxray.oxml.trans.st.enums import (
    SE_PRESET_COLOR_VAL,
    SE_SCHEME_COLOR_VAL,
    SE_SYSTEM_COLOR_VAL,
)
from docxray.oxml.trans.st.shared_common import ST_HexColorRGB
from docxray.oxml.trans.xmlchemy import OxmlElement

from .shared import CT_OfficeArtExtensionList

type EG_ColorTransform = CT_PositiveFixedPercentage | CT_ComplementTransform | CT_InverseTransform | CT_GrayscaleTransform | CT_FixedPercentage | CT_PositivePercentage | CT_PositiveFixedAngle | CT_Angle | CT_Percentage | CT_GammaTransform | CT_InverseGammaTransform
EG_COLOR_TRANSFORM_XPATH = (
    "a:tint | a:shade | a:comp | a:inv | a:gray | a:alpha | a:alphaOff | "
    "a:alphaMod | a:hue | a:hueOff | a:hueMod | a:sat | a:satOff | a:satMod | "
    "a:lum | a:lumOff | a:lumMod | a:red | a:redOff | a:redMod | "
    "a:green | a:greenOff | a:greenMod | a:blue | a:blueOff | a:blueMod | "
    "a:gamma | a:invGamma"
)


class ColorTransform(OxmlElement):
    @cached_property
    def inner_content_items(self) -> EG_ColorTransform:
        return self.xpath(EG_COLOR_TRANSFORM_XPATH)


class CT_PositiveFixedPercentage(OxmlElement):
    @cached_property
    def val(self) -> int | str:
        return self.attr_required(NoNS.VAL, ST_PositiveFixedPercentage)


class CT_ComplementTransform(OxmlElement):
    pass


class CT_InverseTransform(OxmlElement):
    pass


class CT_GrayscaleTransform(OxmlElement):
    pass


class CT_FixedPercentage(OxmlElement):
    @cached_property
    def val(self) -> int | str:
        return self.attr_required(NoNS.VAL, ST_FixedPercentage)


class CT_PositivePercentage(OxmlElement):
    @cached_property
    def val(self) -> int | str:
        return self.attr_required(NoNS.VAL, ST_PositivePercentage)


class CT_PositiveFixedAngle(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(NoNS.VAL, ST_PositiveFixedAngle)


class CT_Angle(OxmlElement):
    @cached_property
    def val(self) -> int:
        return self.attr_required(NoNS.VAL, ST_Angle)


class CT_Percentage(OxmlElement):
    @cached_property
    def val(self) -> int | str:
        return self.attr_required(NoNS.VAL, ST_Percentage)


class CT_GammaTransform(OxmlElement):
    pass


class CT_InverseGammaTransform(OxmlElement):
    pass


class CT_ScRgbColor(ColorTransform):
    @cached_property
    def r(self) -> int | str:
        return self.attr_required(NoNS.R, ST_Percentage)

    @cached_property
    def g(self) -> int | str:
        return self.attr_required(NoNS.G, ST_Percentage)

    @cached_property
    def b(self) -> int | str:
        return self.attr_required(NoNS.B, ST_Percentage)


class CT_SRgbColor(ColorTransform):
    @cached_property
    def val(self) -> bytes:
        return self.attr_required(NoNS.VAL, ST_HexColorRGB)


class CT_HslColor(ColorTransform):
    @cached_property
    def hue(self) -> int:
        return self.attr_required(NoNS.HUE, ST_PositiveFixedAngle)

    @cached_property
    def sat(self) -> int | str:
        return self.attr_required(NoNS.SAT, ST_Percentage)

    @cached_property
    def lum(self) -> int | str:
        return self.attr_required(NoNS.LUM, ST_Percentage)


class CT_SystemColor(ColorTransform):
    @cached_property
    def val(self) -> SE_SYSTEM_COLOR_VAL:
        return self.attr_required(NoNS.VAL, ST_SystemColorVal)

    @cached_property
    def lastClr(self) -> bytes | None:
        return self.attr_optional(NoNS.LAST_CLR, ST_HexColorRGB)


class CT_SchemeColor(ColorTransform):
    @cached_property
    def val(self) -> SE_SCHEME_COLOR_VAL:
        return self.attr_required(NoNS.VAL, ST_SchemeColorVal)


class CT_PresetColor(ColorTransform):
    @cached_property
    def val(self) -> SE_PRESET_COLOR_VAL:
        return self.attr_required(NoNS.VAL, ST_PresetColorVal)


class CT_Color_Theme(OxmlElement):
    @cached_property
    def scrgbClr(self) -> CT_ScRgbColor:
        return self.child_exactly_one(A.SCRGB_CLR, CT_ScRgbColor)

    @cached_property
    def srgbClr(self) -> CT_SRgbColor:
        return self.child_exactly_one(A.SRGB_CLR, CT_SRgbColor)

    @cached_property
    def hslClr(self) -> CT_HslColor:
        return self.child_exactly_one(A.HSL_CLR, CT_HslColor)

    @cached_property
    def sysClr(self) -> CT_SystemColor:
        return self.child_exactly_one(A.SYS_CLR, CT_SystemColor)

    @cached_property
    def schemeClr(self) -> CT_SchemeColor:
        return self.child_exactly_one(A.SCHEME_CLR, CT_SchemeColor)

    @cached_property
    def prstClr(self) -> CT_PresetColor:
        return self.child_exactly_one(A.PRST_CLR, CT_PresetColor)


class CT_ColorScheme(OxmlElement):
    @cached_property
    def name(self) -> str:
        return self.attr_required(NoNS.NAME)

    @cached_property
    def dk1(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.DK1, CT_Color_Theme)

    @cached_property
    def lt1(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.LT1, CT_Color_Theme)

    @cached_property
    def dk2(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.DK2, CT_Color_Theme)

    @cached_property
    def lt2(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.LT2, CT_Color_Theme)

    @cached_property
    def accent1(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.ACCENT1, CT_Color_Theme)

    @cached_property
    def accent2(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.ACCENT2, CT_Color_Theme)

    @cached_property
    def accent3(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.ACCENT3, CT_Color_Theme)

    @cached_property
    def accent4(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.ACCENT4, CT_Color_Theme)

    @cached_property
    def accent5(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.ACCENT5, CT_Color_Theme)

    @cached_property
    def accent6(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.ACCENT6, CT_Color_Theme)

    @cached_property
    def hlink(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.HLINK, CT_Color_Theme)

    @cached_property
    def folHlink(self) -> CT_Color_Theme:
        return self.child_exactly_one(A.FOL_HLINK, CT_Color_Theme)

    @cached_property
    def extLst(self) -> CT_OfficeArtExtensionList | None:
        return self.child_zero_or_one(A.EXT_LST, CT_OfficeArtExtensionList)
