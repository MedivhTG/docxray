from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.numbering import (
    CT_AbstractNum,
    CT_Lvl,
    CT_Num,
    CT_Numbering,
    CT_NumLvl,
)
from docxray.shared import ElementProxy
from docxray.types import ProvidesXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.numbering import NumberingPart


class LvlDefinition(ElementProxy[CT_Lvl]):
    pass


class OverrideNum(ElementProxy[CT_NumLvl]):
    pass


class AbstractNum(ElementProxy[CT_AbstractNum]):
    def __init__(
        self, element: CT_AbstractNum, parent: ProvidesXmlPart
    ) -> None:
        super().__init__(element, parent)
        self._cached_lvls: dict[int, LvlDefinition] = {}

    def get_lvl(self, ilvl_val: int) -> LvlDefinition | None:
        lvl = self._cached_lvls.get(ilvl_val)
        if lvl is not None:
            return lvl
        lvl_elm = self.element.lvl_by_ilvl(ilvl_val)
        if lvl_elm is None:
            return None
        lvl = LvlDefinition(lvl_elm, self)
        self._cached_lvls[ilvl_val] = lvl
        return lvl


class Num(ElementProxy[CT_Num]):
    def __init__(self, element: CT_Num, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_overrides: dict[int, OverrideNum] = {}
        self._cached_abstracts: dict[int, AbstractNum] = {}

    def get_override_num(self, ilvl_val: int) -> OverrideNum | None:
        override_num = self._cached_overrides.get(ilvl_val)
        if override_num is not None:
            return override_num
        numLvl_elm = self.element.override_num_by_ilvl(ilvl_val)
        if numLvl_elm is None:
            return None
        override_num = OverrideNum(numLvl_elm, self)
        self._cached_overrides[ilvl_val] = override_num
        return override_num

    def get_abstract_num(self, abstract_num_id: int) -> AbstractNum | None:
        abstract_num = self._cached_abstracts.get(abstract_num_id)
        if abstract_num is not None:
            return abstract_num
        abstractNum_elm = self.element.abstract_num_by_id(abstract_num_id)
        if abstractNum_elm is None:
            return None
        abstract_num = AbstractNum(abstractNum_elm, self)
        self._cached_abstracts[abstract_num_id] = abstract_num
        return abstract_num


class Numbering(ElementProxy[CT_Numbering]):
    def __init__(self, element: CT_Numbering, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_nums: dict[int, Num] = {}

    @property
    def part(self) -> NumberingPart:
        return self.part

    def get_num(self, numId_val: int) -> Num | None:
        num = self._cached_nums.get(numId_val)
        if num is not None:
            return num
        num_elm = self.element.num_by_id(numId_val)
        if num_elm is None:
            return None
        num = Num(num_elm, self)
        self._cached_nums[numId_val] = num
        return num
