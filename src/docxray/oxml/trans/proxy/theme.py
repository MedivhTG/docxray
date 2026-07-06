from __future__ import annotations

import colorsys
import sys
from collections.abc import Callable
from functools import cached_property
from typing import cast

import webcolors

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.oxml.trans.enums import WIN32_COLOR
from docxray.oxml.trans.package import TransitionalPackage
from docxray.oxml.trans.proxy.compute import percentage
from docxray.oxml.trans.proxy.settings import SemanticColor
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.st.enums import (
    SE_SCHEME_COLOR_VAL,
    SE_SYSTEM_COLOR_VAL,
    SE_THEME_COLOR,
    SE_WML_COLOR_SCHEME_INDEX,
)
from docxray.oxml.trans.theme.color import (
    CT_Color_Theme,
    CT_HslColor,
    CT_PresetColor,
    CT_SchemeColor,
    CT_ScRgbColor,
    CT_SRgbColor,
    CT_SystemColor,
)
from docxray.oxml.trans.theme.font import CT_SupplementalFont, CT_TextFont
from docxray.oxml.trans.theme.theme import CT_OfficeStyleSheet
from docxray.shared import win32_color_hex

SCHEME_GET_COLOR_MAPPING = {
    SE_WML_COLOR_SCHEME_INDEX.LIGHT1: "lt1",
    SE_WML_COLOR_SCHEME_INDEX.DARK1: "dk1",
    SE_WML_COLOR_SCHEME_INDEX.LIGHT2: "lt2",
    SE_WML_COLOR_SCHEME_INDEX.DARK2: "dk2",
    SE_WML_COLOR_SCHEME_INDEX.ACCENT1: "accent1",
    SE_WML_COLOR_SCHEME_INDEX.ACCENT2: "accent2",
    SE_WML_COLOR_SCHEME_INDEX.ACCENT3: "accent3",
    SE_WML_COLOR_SCHEME_INDEX.ACCENT4: "accent4",
    SE_WML_COLOR_SCHEME_INDEX.ACCENT5: "accent5",
    SE_WML_COLOR_SCHEME_INDEX.ACCENT6: "accent6",
    SE_WML_COLOR_SCHEME_INDEX.HYPERLINK: "hlink",
    SE_WML_COLOR_SCHEME_INDEX.FOLLOWED_HYPERLINK: "folHlink",
}

SCHEME_TO_THEME_COLOR = {
    SE_SCHEME_COLOR_VAL.BG1: SE_THEME_COLOR.BACKGROUND1,
    SE_SCHEME_COLOR_VAL.TX1: SE_THEME_COLOR.TEXT1,
    SE_SCHEME_COLOR_VAL.BG2: SE_THEME_COLOR.BACKGROUND2,
    SE_SCHEME_COLOR_VAL.TX2: SE_THEME_COLOR.TEXT2,
    SE_SCHEME_COLOR_VAL.ACCENT1: SE_THEME_COLOR.ACCENT1,
    SE_SCHEME_COLOR_VAL.ACCENT2: SE_THEME_COLOR.ACCENT2,
    SE_SCHEME_COLOR_VAL.ACCENT3: SE_THEME_COLOR.ACCENT3,
    SE_SCHEME_COLOR_VAL.ACCENT4: SE_THEME_COLOR.ACCENT4,
    SE_SCHEME_COLOR_VAL.ACCENT5: SE_THEME_COLOR.ACCENT5,
    SE_SCHEME_COLOR_VAL.ACCENT6: SE_THEME_COLOR.ACCENT6,
    SE_SCHEME_COLOR_VAL.HLINK: SE_THEME_COLOR.HYPERLINK,
    SE_SCHEME_COLOR_VAL.FOL_HLINK: SE_THEME_COLOR.FOLLOWED_HYPERLINK,
    SE_SCHEME_COLOR_VAL.DK1: SE_THEME_COLOR.DARK1,
    SE_SCHEME_COLOR_VAL.LT1: SE_THEME_COLOR.LIGHT1,
    SE_SCHEME_COLOR_VAL.DK2: SE_THEME_COLOR.DARK2,
    SE_SCHEME_COLOR_VAL.LT2: SE_THEME_COLOR.LIGHT2,
}


SYSTEM_COLOR_MAP_WIN32 = {
    SE_SYSTEM_COLOR_VAL.SCROLL_BAR: WIN32_COLOR.SCROLLBAR,
    SE_SYSTEM_COLOR_VAL.BACKGROUND: WIN32_COLOR.BACKGROUND,
    SE_SYSTEM_COLOR_VAL.ACTIVE_CAPTION: WIN32_COLOR.ACTIVECAPTION,
    SE_SYSTEM_COLOR_VAL.INACTIVE_CAPTION: WIN32_COLOR.INACTIVECAPTION,
    SE_SYSTEM_COLOR_VAL.MENU: WIN32_COLOR.MENU,
    SE_SYSTEM_COLOR_VAL.WINDOW: WIN32_COLOR.WINDOW,
    SE_SYSTEM_COLOR_VAL.WINDOW_FRAME: WIN32_COLOR.WINDOWFRAME,
    SE_SYSTEM_COLOR_VAL.MENU_TEXT: WIN32_COLOR.MENUTEXT,
    SE_SYSTEM_COLOR_VAL.WINDOW_TEXT: WIN32_COLOR.WINDOWTEXT,
    SE_SYSTEM_COLOR_VAL.CAPTION_TEXT: WIN32_COLOR.CAPTIONTEXT,
    SE_SYSTEM_COLOR_VAL.ACTIVE_BORDER: WIN32_COLOR.ACTIVEBORDER,
    SE_SYSTEM_COLOR_VAL.INACTIVE_BORDER: WIN32_COLOR.INACTIVEBORDER,
    SE_SYSTEM_COLOR_VAL.APP_WORKSPACE: WIN32_COLOR.APPWORKSPACE,
    SE_SYSTEM_COLOR_VAL.HIGHLIGHT: WIN32_COLOR.HIGHLIGHT,
    SE_SYSTEM_COLOR_VAL.HIGHLIGHT_TEXT: WIN32_COLOR.HIGHLIGHTTEXT,
    SE_SYSTEM_COLOR_VAL.BTN_FACE: WIN32_COLOR.BTNFACE,
    SE_SYSTEM_COLOR_VAL.BTN_SHADOW: WIN32_COLOR.BTNSHADOW,
    SE_SYSTEM_COLOR_VAL.GRAY_TEXT: WIN32_COLOR.GRAYTEXT,
    SE_SYSTEM_COLOR_VAL.BTN_TEXT: WIN32_COLOR.BTNTEXT,
    SE_SYSTEM_COLOR_VAL.INACTIVE_CAPTION_TEXT: WIN32_COLOR.INACTIVECAPTIONTEXT,
    SE_SYSTEM_COLOR_VAL.BTN_HIGHLIGHT: WIN32_COLOR.BTNHIGHLIGHT,
    SE_SYSTEM_COLOR_VAL.D_3D_DK_SHADOW: WIN32_COLOR.C_3DDKSHADOW,
    SE_SYSTEM_COLOR_VAL.D_3D_LIGHT: WIN32_COLOR.C_3DLIGHT,
    SE_SYSTEM_COLOR_VAL.INFO_TEXT: WIN32_COLOR.INFOTEXT,
    SE_SYSTEM_COLOR_VAL.INFO_BK: WIN32_COLOR.INFOBK,
    SE_SYSTEM_COLOR_VAL.HOT_LIGHT: WIN32_COLOR.HOTLIGHT,
    SE_SYSTEM_COLOR_VAL.GRADIENT_ACTIVE_CAPTION: WIN32_COLOR.GRADIENTACTIVECAPTION,
    SE_SYSTEM_COLOR_VAL.GRADIENT_INACTIVE_CAPTION: WIN32_COLOR.GRADIENTINACTIVECAPTION,
    SE_SYSTEM_COLOR_VAL.MENU_HIGHLIGHT: WIN32_COLOR.MENUHIGHLIGHT,
    SE_SYSTEM_COLOR_VAL.MENU_BAR: WIN32_COLOR.MENUBAR,
}

SYSTEM_COLOR_DEFAULTS = {
    SE_SYSTEM_COLOR_VAL.SCROLL_BAR: "#C8C8C8",
    SE_SYSTEM_COLOR_VAL.BACKGROUND: "#6A6A6A",
    SE_SYSTEM_COLOR_VAL.ACTIVE_CAPTION: "#0054E3",
    SE_SYSTEM_COLOR_VAL.INACTIVE_CAPTION: "#7A7A7A",
    SE_SYSTEM_COLOR_VAL.MENU: "#F0F0F0",
    SE_SYSTEM_COLOR_VAL.WINDOW: "#FFFFFF",
    SE_SYSTEM_COLOR_VAL.WINDOW_FRAME: "#000000",
    SE_SYSTEM_COLOR_VAL.MENU_TEXT: "#000000",
    SE_SYSTEM_COLOR_VAL.WINDOW_TEXT: "#000000",
    SE_SYSTEM_COLOR_VAL.CAPTION_TEXT: "#FFFFFF",
    SE_SYSTEM_COLOR_VAL.ACTIVE_BORDER: "#B4B4B4",
    SE_SYSTEM_COLOR_VAL.INACTIVE_BORDER: "#B4B4B4",
    SE_SYSTEM_COLOR_VAL.APP_WORKSPACE: "#ABABAB",
    SE_SYSTEM_COLOR_VAL.HIGHLIGHT: "#0078D7",
    SE_SYSTEM_COLOR_VAL.HIGHLIGHT_TEXT: "#FFFFFF",
    SE_SYSTEM_COLOR_VAL.BTN_FACE: "#F0F0F0",
    SE_SYSTEM_COLOR_VAL.BTN_SHADOW: "#A0A0A0",
    SE_SYSTEM_COLOR_VAL.GRAY_TEXT: "#6D6D6D",
    SE_SYSTEM_COLOR_VAL.BTN_TEXT: "#000000",
    SE_SYSTEM_COLOR_VAL.INACTIVE_CAPTION_TEXT: "#FFFFFF",
    SE_SYSTEM_COLOR_VAL.BTN_HIGHLIGHT: "#D5D5D5",
    SE_SYSTEM_COLOR_VAL.D_3D_DK_SHADOW: "#696969",
    SE_SYSTEM_COLOR_VAL.D_3D_LIGHT: "#D5D5D5",
    SE_SYSTEM_COLOR_VAL.INFO_TEXT: "#000000",
    SE_SYSTEM_COLOR_VAL.INFO_BK: "#FFFFE1",
    SE_SYSTEM_COLOR_VAL.HOT_LIGHT: "#0078D7",
    SE_SYSTEM_COLOR_VAL.GRADIENT_ACTIVE_CAPTION: "#B9D1EA",
    SE_SYSTEM_COLOR_VAL.GRADIENT_INACTIVE_CAPTION: "#D7D7D7",
    SE_SYSTEM_COLOR_VAL.MENU_HIGHLIGHT: "#0078D7",
    SE_SYSTEM_COLOR_VAL.MENU_BAR: "#F0F0F0",
}


# TODO: look fo other propertes
class FontFamily(ElementProxy[CT_TextFont]):
    @cached_property
    def typeface(self) -> str:
        return self.element.typeface


# TODO: look fo other propertes
class FontFamilySupplemental(ElementProxy[CT_SupplementalFont]):
    @cached_property
    def typeface(self) -> str:
        return self.element.typeface

    @cached_property
    def script(self) -> str:
        return self.element.script


class ThemeColor(ElementProxy[CT_Color_Theme]):
    @cached_property
    def parent(self) -> Theme:
        return cast("Theme", self._parent)

    @cached_property
    def color(self) -> str | None:
        mapping: dict[str, Callable] = {
            "scrgbClr": self._rgb_pct,
            "srgbClr": self._rgb,
            "hslClr": self._hsl,
            "sysClr": self._sys,
            "schemeClr": self._scheme,
            "prstClr": self._preset,
        }
        for attr_name, func in mapping.items():
            try:
                clr_elm = getattr(self.element, attr_name)
                clr_hex: str | None = func(clr_elm)
                if clr_hex is None:
                    return clr_hex
                return clr_hex.upper()
            except InvalidXmlError:
                continue
        return None

    def _rgb_pct(self, scrgbClr_elm: CT_ScRgbColor) -> str:
        def _hex(pct: int | str) -> str:
            clr_float = percentage(pct) or 0.0
            return f"{round(clr_float * 255):02X}"

        return f"#{_hex(scrgbClr_elm.r)}{_hex(scrgbClr_elm.g)}{_hex(scrgbClr_elm.b)}"

    def _rgb(self, srgbClr_elm: CT_SRgbColor) -> str:
        return f"#{srgbClr_elm.val.hex()}"

    def _hsl(self, hslClr_elm: CT_HslColor) -> str:
        hue_norm = hslClr_elm.hue / 60000.0 / 360.0
        luminance = percentage(hslClr_elm.lum) or 0.0
        saturation = percentage(hslClr_elm.sat) or 0.0
        r, g, b = colorsys.hls_to_rgb(hue_norm, luminance, saturation)
        return f"#{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}"

    def _sys(self, sysClr_elm: CT_SystemColor) -> str:
        if sysClr_elm.lastClr:
            return f"#{sysClr_elm.lastClr.hex()}"
        if sys.platform == "win32":
            idx = SYSTEM_COLOR_MAP_WIN32[sysClr_elm.val]
            return win32_color_hex(idx)
        return SYSTEM_COLOR_DEFAULTS[sysClr_elm.val]

    def _scheme(self, schemeClr_elm: CT_SchemeColor) -> str | None:
        if schemeClr_elm.val == "phClr":
            return None
        clr = SCHEME_TO_THEME_COLOR[schemeClr_elm.val]
        return self.parent.palette[clr].color

    def _preset(self, prstClr: CT_PresetColor) -> str:
        return webcolors.name_to_hex(prstClr.val.value)


class Theme(ElementProxy[CT_OfficeStyleSheet]):
    @cached_property
    def major_latin(self) -> FontFamily:
        return FontFamily(
            self.element.themeElements.fontScheme.majorFont.latin, self
        )

    @cached_property
    def major_east_asia(self) -> FontFamily:
        return FontFamily(
            self.element.themeElements.fontScheme.majorFont.ea, self
        )

    @cached_property
    def major_complex_script(self) -> FontFamily:
        return FontFamily(
            self.element.themeElements.fontScheme.majorFont.cs, self
        )

    @cached_property
    def major_fonts(self) -> list[FontFamilySupplemental]:
        return [
            FontFamilySupplemental(f, self)
            for f in self.element.themeElements.fontScheme.majorFont.font
        ]

    @cached_property
    def minor_latin(self) -> FontFamily:
        return FontFamily(
            self.element.themeElements.fontScheme.minorFont.latin, self
        )

    @cached_property
    def minor_east_asia(self) -> FontFamily:
        return FontFamily(
            self.element.themeElements.fontScheme.minorFont.ea, self
        )

    @cached_property
    def minor_complex_script(self) -> FontFamily:
        return FontFamily(
            self.element.themeElements.fontScheme.minorFont.cs, self
        )

    @cached_property
    def minor_fonts(self) -> list[FontFamilySupplemental]:
        return [
            FontFamilySupplemental(f, self)
            for f in self.element.themeElements.fontScheme.minorFont.font
        ]

    @cached_property
    def palette(self) -> dict[SE_THEME_COLOR, ThemeColor]:
        def _color(name: SemanticColor) -> ThemeColor:
            idx = mapping[name]
            attr_name = SCHEME_GET_COLOR_MAPPING[idx]
            return ThemeColor(getattr(clrScheme_elm, attr_name), self)

        C = SE_THEME_COLOR
        clrScheme_elm = self.element.themeElements.clrScheme
        settings = cast(
            "TransitionalPackage", self.part.package
        ).main_document_part.settings
        mapping = settings.theme_color_mapping

        return {
            C.DARK1: ThemeColor(clrScheme_elm.dk1, self),
            C.LIGHT1: ThemeColor(clrScheme_elm.lt1, self),
            C.DARK2: ThemeColor(clrScheme_elm.dk2, self),
            C.LIGHT2: ThemeColor(clrScheme_elm.lt2, self),
            C.ACCENT1: _color("accent1"),
            C.ACCENT2: _color("accent2"),
            C.ACCENT3: _color("accent3"),
            C.ACCENT4: _color("accent4"),
            C.ACCENT5: _color("accent5"),
            C.ACCENT6: _color("accent6"),
            C.HYPERLINK: _color("hyperlink"),
            C.FOLLOWED_HYPERLINK: _color("followedHyperlink"),
            C.BACKGROUND1: _color("bg1"),
            C.TEXT1: _color("t1"),
            C.BACKGROUND2: _color("bg2"),
            C.TEXT2: _color("t2"),
        }
