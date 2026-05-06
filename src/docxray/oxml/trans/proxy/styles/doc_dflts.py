from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.styles import CT_DocDefaults

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.styles import StylesPart


class DocumentDefaults(ElementProxy[CT_DocDefaults]):
    @property
    def part(self) -> StylesPart:
        return self.part
