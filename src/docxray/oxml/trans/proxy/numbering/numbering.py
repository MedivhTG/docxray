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
    CT_NumLvl,
)
from docxray.oxml.trans.proxy.shared import (
    ElementProxy,
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import (
    NumberingStyle,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.styles.styles import Styles
from docxray.oxml.trans.proxy.types import ProvidesXmlPart
from docxray.oxml.trans.st.enums import SE_JC, SE_LEVEL_SUFFIX, SE_StyleType

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.numbering import NumberingPart


class Level(ElementProxy[CT_Lvl]):
    @cached_property
    def paragraph_style(self) -> ParagraphStyle | None:
        """Paragraph style linked to level itself.

        If here is pStyle element inside, but referenced paragraph
        style has numPr element, than `None` returned instead
        (numbering cannot related to para style with back ref).

        Returns:
            ParagraphStyle | None: Paragraph style or None of not exist (or other case).
        """
        pStyle_elm = self.element.pStyle
        if pStyle_elm is None:
            return None
        style = self.parent.numbering.styles.get_by_id(
            pStyle_elm.val, SE_StyleType.PARAGRAPH, ParagraphStyle
        )
        pPr_elm = style.element.pPr
        if pPr_elm is not None:
            if pPr_elm.numPr is not None:
                return None
        return style

    @cached_property
    def parent(self) -> AbstractNum | LevelOverride:
        return cast("AbstractNum | LevelOverride", self._parent)

    @cached_property
    def ilvl(self) -> int:
        return self._element.ilvl

    @cached_property
    def locale(self) -> str | None:
        locale = safe_get_prop(
            self._element, PropertyPath.base("val", "rPr.lang"), False
        )
        if isinstance(locale, NotFound):
            return None
        return locale

    @cached_property
    def alignment(self) -> SE_JC:
        if self._element.lvlJc is None:
            return SE_JC.LEFT
        return self._element.lvlJc.val

    @cached_property
    def separator(self) -> SE_LEVEL_SUFFIX:
        if self._element.suff is None:
            return SE_LEVEL_SUFFIX.TAB
        return self._element.suff.val


class LevelOverride(ElementProxy[CT_NumLvl]):
    @cached_property
    def num(self) -> Num:
        return cast("Num", self._parent)

    @cached_property
    def numbering(self) -> Numbering:
        return self.num.numbering

    @cached_property
    def restart_from(self) -> int | None:
        startOverride_elm = self.element.startOverride
        if startOverride_elm is None:
            return None
        return startOverride_elm.val

    @cached_property
    def lvl(self) -> Level | None:
        lvl_elm = self.element.lvl
        if lvl_elm is None:
            return None
        return Level(lvl_elm, self)


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

    def lvl_by_ilvl(self, ilvl: int) -> Level:
        if lvl := self._cached_lvls.get(ilvl):
            return lvl
        lvl_elm = self.element.lvl_by_ilvl(ilvl)
        if lvl_elm is None:
            msg = f"No associated level for {ilvl}"
            raise InvalidXmlError(msg)
        lvl = Level(lvl_elm, self)
        self._cached_lvls[ilvl] = lvl
        return lvl

    def lvl_by_para_style(self, style_id: str) -> Level:
        for lvl in self._cached_lvls.values():
            pStyle_elm = lvl.element.pStyle
            if pStyle_elm is not None and pStyle_elm.val == style_id:
                return lvl
        lvl_elm = self.element.lvl_by_para_style(style_id)
        if lvl_elm is None:
            msg = f"No associated level for {style_id}"
            raise InvalidXmlError(msg)
        lvl = Level(lvl_elm, self)
        self._cached_lvls[lvl_elm.ilvl] = lvl
        return lvl


class Num(ElementProxy[CT_Num]):
    def __init__(self, element: CT_Num, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_lvl_overrides: dict[int, LevelOverride] = {}

    @cached_property
    def numbering(self) -> Numbering:
        return cast("Numbering", self._parent)

    @cached_property
    def abstract_num(self) -> AbstractNum:
        return self.numbering.get_abstract_num(self.element.abstractNumId.val)

    def associated_lvl_override(self, ilvl: int) -> LevelOverride | None:
        if lvl_override := self._cached_lvl_overrides.get(ilvl):
            return lvl_override
        overrideLvl_elm = self.element.override_num_by_ilvl(ilvl)
        if overrideLvl_elm is None:
            return None
        lvl_override = LevelOverride(overrideLvl_elm, self)
        self._cached_lvl_overrides[ilvl] = lvl_override
        return lvl_override


class Numbering(ElementProxy[CT_Numbering]):
    def __init__(self, element: CT_Numbering, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_nums: dict[int, Num] = {}
        self._cached_abstract_nums: dict[int, AbstractNum] = {}

    @property
    def part(self) -> NumberingPart:
        return cast("NumberingPart", self._parent)

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

    def associated_lvl(self, num_id: int, ilvl: int) -> Level:
        num = self.get_num(num_id)
        lvl_override = num.associated_lvl_override(ilvl)
        if lvl_override is not None:
            lvl = lvl_override.lvl
            if lvl is not None:
                return lvl
        return num.abstract_num.lvl_by_ilvl(ilvl)
