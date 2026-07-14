from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.t.proxy.base import ElementProxy, NotFound
from docxray.oxml.t.proxy.text.font import Font
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.styles import CT_DocDefaults

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.parts.styles import StylesPart


class DocumentDefaults(ElementProxy[CT_DocDefaults]):
    @cached_property
    def part(self) -> StylesPart:
        return self.part

    @cached_property
    def language(self) -> Language | None:
        locale = self.prop("rPrDefault.rPr.lang")
        if isinstance(locale, NotFound):
            return None
        return locale

    @cached_property
    def font(self) -> Font | None:
        font = self.prop("rPrDefault.rPr.rFonts")
        if isinstance(font, NotFound):
            return None
        return font
