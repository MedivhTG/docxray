"""Style object hierarchy."""

from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.styles import CT_Style
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
        return self.part


class CharacterStyle(BaseStyle):
    pass


class ParagraphStyle(CharacterStyle):
    pass


class TableStyle(ParagraphStyle):
    pass


class NumberingStyle(BaseStyle):
    pass
