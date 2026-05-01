from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.numbering import CT_Numbering
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.numbering import NumberingPart


class Numbering(ElementProxy[CT_Numbering]):
    @property
    def part(self) -> NumberingPart:
        return self.part
