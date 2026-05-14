from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.exceptions import InvalidXmlError
from docxray.oxml.trans.numbering import (
    CT_AbstractNum,
    CT_Lvl,
    CT_Num,
    CT_Numbering,
)
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.proxy.styles.style import NumberingStyle
from docxray.oxml.trans.proxy.styles.styles import Styles
from docxray.oxml.trans.proxy.types import ProvidesXmlPart
from docxray.oxml.trans.st.enums import SE_StyleType

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.numbering import NumberingPart


class Level(ElementProxy[CT_Lvl]):
    pass


class AbstractNum(ElementProxy[CT_AbstractNum]):
    def __init__(
        self, element: CT_AbstractNum, parent: ProvidesXmlPart
    ) -> None:
        super().__init__(element, parent)
        self._cached_lvls: dict[int, Level] = {}

    @cached_property
    def numbering(self) -> Numbering:
        return cast("Numbering", self._parent)

    @cached_property
    def numbering_style(self) -> NumberingStyle | None:
        """This style is `not None` if abstract numbering
        do not contains info about properties of list items and
        those properties must be resolved from style hierarchy
        and back referenced numbering definitions.
        """
        style_id = self.element.numStyleLink
        if style_id is None:
            return None
        return self.numbering.styles.get_by_id(
            style_id.val, SE_StyleType.NUMBERING, NumberingStyle
        )

    def lvl_by_ilvl(self, ilvl: int):
        if lvl := self._cached_lvls.get(ilvl):
            return lvl
        lvl_elm = self.element.lvl_by_ilvl(ilvl)
        if lvl_elm is None:
            return None
        lvl = Level(lvl_elm, self)
        self._cached_lvls[ilvl] = lvl
        return lvl


class Num(ElementProxy[CT_Num]):
    @cached_property
    def numbering(self) -> Numbering:
        return cast("Numbering", self._parent)

    @cached_property
    def abstract_num(self) -> AbstractNum:
        return self.numbering.get_abstract_num(self.element.abstractNumId.val)


class Numbering(ElementProxy[CT_Numbering]):
    def __init__(self, element: CT_Numbering, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_nums: dict[int, Num] = {}
        self._cached_abstract_nums: dict[int, AbstractNum] = {}

    @property
    def part(self) -> NumberingPart:
        return self.part

    @cached_property
    def styles(self) -> Styles:
        return self.part.styles

    def get_num(self, num_id: int) -> Num:
        if num := self._cached_nums.get(num_id):
            return num
        num_elm = self.element.num_by_id(num_id)
        if num_elm is None:
            msg = "Referenced num not found"
            raise InvalidXmlError(msg)
        num = Num(num_elm, self)
        self._cached_nums[num_id] = num
        return num

    def get_abstract_num(self, abstract_num_id: int) -> AbstractNum:
        if abstract_num := self._cached_abstract_nums.get(abstract_num_id):
            return abstract_num
        abstractNum_elm = self.element.abstract_num_by_id(abstract_num_id)
        if abstractNum_elm is None:
            msg = "Referenced abstract num not found"
            raise InvalidXmlError(msg)
        abstract_num = AbstractNum(abstractNum_elm, self)
        self._cached_abstract_nums[abstract_num_id] = abstract_num
        return abstract_num

    def associated_lvl(self, num_id: int, ilvl: int) -> Level | None:
        num = self.get_num(num_id)
        return num.abstract_num.lvl_by_ilvl(ilvl)
