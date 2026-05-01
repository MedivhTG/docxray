from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.styles import CT_DocDefaults
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.styles import StylesPart


class DocumentDefaults(ElementProxy[CT_DocDefaults]):
    @property
    def part(self) -> StylesPart:
        return self.part
