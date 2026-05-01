"""Style object hierarchy."""

from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.styles import CT_Style
from docxray.shared import PartProxy

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


class BaseStyle(PartProxy[CT_Style, "StylesPart"]):
    pass


class CharacterStyle(BaseStyle):
    pass


class ParagraphStyle(CharacterStyle):
    pass


class TableStyle(ParagraphStyle):
    pass


class NumberingStyle(BaseStyle):
    pass
