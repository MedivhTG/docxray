"""Style object hierarchy."""

from __future__ import annotations

from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.styles import CT_Style
from docx.shared import ElementProxy


def StyleFactory(style_elm: CT_Style) -> BaseStyle:
    """Return `Style` object of appropriate |BaseStyle| subclass for `style_elm`."""
    style_cls: type[BaseStyle] = {
        WD_STYLE_TYPE.PARAGRAPH: ParagraphStyle,
        WD_STYLE_TYPE.CHARACTER: CharacterStyle,
        WD_STYLE_TYPE.TABLE: TableStyle,
        WD_STYLE_TYPE.LIST: NumberingStyle,
        None: BaseStyle,
    }[style_elm.type]

    return style_cls(style_elm)


class BaseStyle(ElementProxy[CT_Style]):
    pass


class CharacterStyle(BaseStyle):
    pass


class ParagraphStyle(CharacterStyle):
    pass


class TableStyle(ParagraphStyle):
    pass


class NumberingStyle(BaseStyle):
    pass
