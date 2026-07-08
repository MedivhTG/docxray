from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.t.proxy.base import (
    ElementProxy,
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.t.styles import CT_DocDefaults

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.parts.styles import StylesPart


class DocumentDefaults(ElementProxy[CT_DocDefaults]):
    @cached_property
    def part(self) -> StylesPart:
        return self.part

    @cached_property
    def locale(self) -> str | None:
        locale = safe_get_prop(
            self.element,
            PropertyPath.base("val", "rPrDefault.rPr.lang"),
            False,
        )
        if isinstance(locale, NotFound):
            return None
        return locale
