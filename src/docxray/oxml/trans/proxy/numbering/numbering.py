from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.trans.numbering import CT_Num, CT_Numbering
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.proxy.types import ProvidesXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.numbering import NumberingPart


class Numbering(ElementProxy[CT_Numbering]):
    def __init__(self, element: CT_Numbering, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_nums: dict[int, CT_Num] = {}

    @property
    def part(self) -> NumberingPart:
        return self.part

    def get_num(self, num_id: int) -> CT_Num | None:
        if num_elm := self._cached_nums.get(num_id):
            return num_elm
        num_elm = self.element.num_by_id(num_id)
        if num_elm is not None:
            self._cached_nums[num_id] = num_elm
            return num_elm
        return None
