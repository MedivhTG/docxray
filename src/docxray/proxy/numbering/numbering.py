from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.transitional.numbering import (
    CT_AbstractNum,
    CT_Lvl,
    CT_Num,
    CT_Numbering,
    CT_NumLvl,
)
from docxray.oxml.transitional.text.num_props import CT_NumPr
from docxray.proxy.shared import ElementProxy
from docxray.proxy.types import ProvidesXmlPart

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.numbering import NumberingPart


class LvlDefinition(ElementProxy[CT_Lvl]):
    pass


class OverrideNum(ElementProxy[CT_NumLvl]):
    @cached_property
    def lvl(self) -> LvlDefinition | None:
        lvl = self.element.lvl
        if lvl is None:
            return None
        return LvlDefinition(lvl, self)


class AbstractNum(ElementProxy[CT_AbstractNum]):
    def __init__(
        self, element: CT_AbstractNum, parent: ProvidesXmlPart
    ) -> None:
        super().__init__(element, parent)
        self._cached_lvls: dict[int, LvlDefinition] = {}

    def get_lvl_by_ilvl(self, ilvl_val: int) -> LvlDefinition | None:
        lvl = self._cached_lvls.get(ilvl_val)
        if lvl is not None:
            return lvl
        lvl_elm = self.element.lvl_by_ilvl(ilvl_val)
        if lvl_elm is None:
            return None
        lvl = LvlDefinition(lvl_elm, self)
        self._cached_lvls[ilvl_val] = lvl
        return lvl

    def get_lvl_by_pstyle(self, pStyle_val: str) -> LvlDefinition | None:
        lvl_elm = self.element.lvl_by_pStyle(pStyle_val)
        if lvl_elm is None:
            return None
        lvl = LvlDefinition(lvl_elm, self)
        self._cached_lvls[lvl_elm.ilvl] = lvl
        return lvl


class Num(ElementProxy[CT_Num]):
    def __init__(self, element: CT_Num, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_overrides: dict[int, OverrideNum] = {}

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


class Numbering(ElementProxy[CT_Numbering]):
    def __init__(self, element: CT_Numbering, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_nums: dict[int, Num] = {}
        self._cached_abstracts: dict[int, AbstractNum] = {}

    @property
    def part(self) -> NumberingPart:
        return self.part

    def get_lvl_proxy(
        self, numPr_elm: CT_NumPr
    ) -> OverrideNum | AbstractNum | None:
        numId_elm = numPr_elm.numId
        if numId_elm is None:
            return None
        num = self.get_num(numId_elm.val)
        if num is None:
            return None
        ilvl_elm = numPr_elm.ilvl
        if ilvl_elm is None:
            return self.get_abstract_num(num.element.abstractNumId.val)
        override_num = num.get_override_num(ilvl_elm.val)
        if override_num is not None:
            return override_num
        return self.get_abstract_num(num.element.abstractNumId.val)

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
