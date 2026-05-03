"""Style object hierarchy."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.styles import CT_Style, CT_Styles
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.styles import StylesPart


def StyleFactory(style_elm: CT_Style, part: StylesPart) -> BaseStyle:
    """Return `Style` object of appropriate |BaseStyle| subclass for `style_elm`."""
    style_cls: type[BaseStyle] = {
        WD_STYLE_TYPE.PARAGRAPH: ParagraphStyle,
        WD_STYLE_TYPE.CHARACTER: CharacterStyle,
        WD_STYLE_TYPE.TABLE: TableStyle,
        WD_STYLE_TYPE.LIST: NumberingStyle,
        None: BaseStyle,
    }[style_elm.type]

    return style_cls(style_elm, part)


class BaseStyle(ElementProxy[CT_Style]):
    @property
    def part(self) -> StylesPart:
        return cast("StylesPart", self._parent)


class CharacterStyle(BaseStyle):
    @cached_property
    def based_on(self) -> str | None:
        basedOn = self.element.basedOn
        if basedOn is None:
            return None
        return basedOn.val

    @cached_property
    def base_style(self) -> BaseStyle | None:
        basedOn = self.based_on
        if basedOn is None:
            return None
        styles_elm = self.element.getparent(CT_Styles)
        if styles_elm is None:
            return None
        style_elm = styles_elm.get_by_id(basedOn)
        if style_elm is None:
            return None
        return StyleFactory(style_elm, self.part)


class ParagraphStyle(CharacterStyle):
    pass


class TableStyle(ParagraphStyle):
    pass


class NumberingStyle(BaseStyle):
    pass
