from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import CT_Language
from docxray.oxml.trans.st.enums import SE_WML_COLOR_SCHEME_INDEX
from docxray.oxml.trans.st.wml import ST_WmlColorSchemeIndex
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_ColorSchemeMapping(OxmlElement):
    @cached_property
    def bg1(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.BG1, ST_WmlColorSchemeIndex)

    @cached_property
    def t1(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.T1, ST_WmlColorSchemeIndex)

    @cached_property
    def bg2(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.BG2, ST_WmlColorSchemeIndex)

    @cached_property
    def t2(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.T2, ST_WmlColorSchemeIndex)

    @cached_property
    def accent1(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.ACCENT1, ST_WmlColorSchemeIndex)

    @cached_property
    def accent2(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.ACCENT2, ST_WmlColorSchemeIndex)

    @cached_property
    def accent3(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.ACCENT3, ST_WmlColorSchemeIndex)

    @cached_property
    def accent4(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.ACCENT4, ST_WmlColorSchemeIndex)

    @cached_property
    def accent5(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.ACCENT5, ST_WmlColorSchemeIndex)

    @cached_property
    def accent6(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.ACCENT6, ST_WmlColorSchemeIndex)

    @cached_property
    def hyperlink(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.HYPERLINK, ST_WmlColorSchemeIndex)

    @cached_property
    def followedHyperlink(self) -> SE_WML_COLOR_SCHEME_INDEX | None:
        return self.attr_optional(W.FOLLOWED_HYPERLINK, ST_WmlColorSchemeIndex)


class CT_Settings(OxmlElement):
    @cached_property
    def themeFontLang(self) -> CT_Language | None:
        return self.child_zero_or_one(W.THEME_FONT_LANG, CT_Language)

    @cached_property
    def clrSchemeMapping(self) -> CT_ColorSchemeMapping | None:
        return self.child_zero_or_one(
            W.CLR_SCHEME_MAPPING, CT_ColorSchemeMapping
        )
