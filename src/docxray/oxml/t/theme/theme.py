from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.t.ns import A
from docxray.oxml.t.xmlchemy import OxmlElement

from .color import CT_ColorScheme
from .font import CT_FontScheme
from .shared import CT_OfficeArtExtensionList


class CT_StyleMatrix(OxmlElement):
    pass


class CT_BaseStyles(OxmlElement):
    @cached_property
    def clrScheme(self) -> CT_ColorScheme:
        return self.child_exactly_one(A.CLR_SCHEME, CT_ColorScheme)

    @cached_property
    def fontScheme(self) -> CT_FontScheme:
        return self.child_exactly_one(A.FONT_SCHEME, CT_FontScheme)

    @cached_property
    def fmtScheme(self) -> CT_StyleMatrix:
        return self.child_exactly_one(A.FMT_SCHEME, CT_StyleMatrix)

    @cached_property
    def extLst(self) -> CT_OfficeArtExtensionList | None:
        return self.child_zero_or_one(A.EXT_LST, CT_OfficeArtExtensionList)


class CT_ObjectStyleDefaults(OxmlElement):
    pass


class CT_ColorSchemeList(OxmlElement):
    pass


class CT_CustomColorList(OxmlElement):
    pass


class CT_OfficeStyleSheet(OxmlElement):
    @cached_property
    def themeElements(self) -> CT_BaseStyles:
        return self.child_exactly_one(A.THEME_ELEMENTS, CT_BaseStyles)

    @cached_property
    def objectDefaults(self) -> CT_ObjectStyleDefaults | None:
        return self.child_zero_or_one(
            A.OBJECT_DEFAULTS, CT_ObjectStyleDefaults
        )

    @cached_property
    def extraClrSchemeLst(self) -> CT_ColorSchemeList | None:
        return self.child_zero_or_one(
            A.EXTRA_CLR_SCHEME_LST, CT_ColorSchemeList
        )

    @cached_property
    def custClrLst(self) -> CT_CustomColorList | None:
        return self.child_zero_or_one(A.CUST_CLR_LST, CT_CustomColorList)

    @cached_property
    def extLst(self) -> CT_OfficeArtExtensionList | None:
        return self.child_zero_or_one(A.EXT_LST, CT_OfficeArtExtensionList)
