"""Style object hierarchy."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.enum.word import WD_CNF_FORMAT
from docxray.oxml.transitional.simple_types.enums import SE_StyleType
from docxray.oxml.transitional.styles import CT_Style, CT_Styles, CT_TblStylePr
from docxray.proxy.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.styles import StylesPart


def StyleFactory(style_elm: CT_Style, part: StylesPart) -> BaseStyle:
    """Return `Style` object of appropriate |BaseStyle| subclass for `style_elm`."""
    style_cls: type[BaseStyle] = {
        SE_StyleType.PARAGRAPH: ParagraphStyle,
        SE_StyleType.CHARACTER: CharacterStyle,
        SE_StyleType.TABLE: TableStyle,
        SE_StyleType.NUMBERING: NumberingStyle,
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
    @cached_property
    def firstRow(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.FIRST_ROW)

    @cached_property
    def lastRow(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.LAST_ROW)

    @cached_property
    def firstCol(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.FIRST_COLUMN)

    @cached_property
    def lastCol(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.LAST_COLUMN)

    @cached_property
    def band1Vert(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.ODD_VERTICAL_BAND)

    @cached_property
    def band2Vert(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.EVEN_VERTICAL_BAND)

    @cached_property
    def band1Horz(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.ODD_HORIZONTAL_BAND)

    @cached_property
    def band2Horz(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND)

    @cached_property
    def nwCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN)

    @cached_property
    def neCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN)

    @cached_property
    def swCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN)

    @cached_property
    def seCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN)

    def bitwise_table_style_property(
        self, flag: WD_CNF_FORMAT
    ) -> CT_TblStylePr | None:
        match flag:
            case WD_CNF_FORMAT.FIRST_ROW:
                return self.firstRow
            case WD_CNF_FORMAT.LAST_ROW:
                return self.lastRow
            case WD_CNF_FORMAT.FIRST_COLUMN:
                return self.firstCol
            case WD_CNF_FORMAT.LAST_COLUMN:
                return self.lastCol
            case WD_CNF_FORMAT.ODD_VERTICAL_BAND:
                return self.band1Vert
            case WD_CNF_FORMAT.EVEN_VERTICAL_BAND:
                return self.band2Vert
            case WD_CNF_FORMAT.ODD_HORIZONTAL_BAND:
                return self.band1Horz
            case WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND:
                return self.band2Horz
            case WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN:
                return self.nwCell
            case WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN:
                return self.neCell
            case WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN:
                return self.swCell
            case WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN:
                return self.seCell

    def tbl_style_prop(self, type: WD_CNF_FORMAT) -> CT_TblStylePr | None:
        return self.element.tblStylePr_for(type)


class NumberingStyle(BaseStyle):
    pass
