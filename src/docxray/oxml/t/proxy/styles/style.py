"""Style object hierarchy."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.oxml.t.enums import WD_CNF_FORMAT
from docxray.oxml.t.proxy.base import (
    ElementProxy,
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.t.st.enums import SE_StyleType, SE_TblStyleOverrideType
from docxray.oxml.t.styles import CT_Style, CT_Styles, CT_TblStylePr

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.parts.styles import StylesPart
    from docxray.oxml.t.proxy.numbering.numbering import Num, Numbering


def StyleFactory(style_elm: CT_Style, part: StylesPart) -> BaseStyle:
    """Return `Style` object of appropriate |BaseStyle| subclass for `style_elm`."""
    return S_TYPE_TO_STYLE_CLS[style_elm.type](style_elm, part)


class BaseStyle(ElementProxy[CT_Style]):
    @property
    def part(self) -> StylesPart:
        return cast("StylesPart", self._parent)

    @property
    def numbering(self) -> Numbering | None:
        return self.part.numbering

    @cached_property
    def name(self) -> str:
        name_elm = self.element.name
        if name_elm is None:
            return ""
        return name_elm.val


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
    def wholeTable(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.ENTIRE_TABLE)

    @cached_property
    def firstRow(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.HEADER_ROW)

    @cached_property
    def lastRow(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.FOOTER_ROW)

    @cached_property
    def firstCol(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.FIRST_COLUMN)

    @cached_property
    def lastCol(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.LAST_COLUMN)

    @cached_property
    def band1Vert(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.VERTICAL_BAND_ODD)

    @cached_property
    def band2Vert(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.VERTICAL_BAND_EVEN)

    @cached_property
    def band1Horz(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TblStyleOverrideType.HORIZONTAL_BAND_ODD)

    @cached_property
    def band2Horz(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TblStyleOverrideType.HORIZONTAL_BAND_EVEN
        )

    @cached_property
    def nwCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TblStyleOverrideType.TOP_LEFT_CORNER_CELL
        )

    @cached_property
    def neCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TblStyleOverrideType.TOP_RIGHT_CORNER_CELL
        )

    @cached_property
    def swCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TblStyleOverrideType.BOTTOM_LEFT_CORNER_CELL
        )

    @cached_property
    def seCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TblStyleOverrideType.BOTTOM_RIGHT_CORNER_CELL
        )

    def bitwise_tbl_style_prop(
        self, flag: WD_CNF_FORMAT
    ) -> CT_TblStylePr | None:
        return getattr(self, flag.format_name(), None)

    def tbl_style_prop(
        self, type: SE_TblStyleOverrideType
    ) -> CT_TblStylePr | None:
        return self.element.tblStylePr_for(type)


class NumberingStyle(BaseStyle):
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

    @cached_property
    def num(self) -> Num:
        err = InvalidXmlError("No associated Num instance for NumberingStyle")
        if self.numbering is None:
            raise err
        path = PropertyPath.base("val", "pPr.numPr.numId")
        num_id = safe_get_prop(self.element, path, False)
        if isinstance(num_id, NotFound):
            raise err
        return self.numbering.get_num(num_id)


S_TYPE_TO_STYLE_CLS: dict[SE_StyleType | None, Any] = {
    SE_StyleType.PARAGRAPH: ParagraphStyle,
    SE_StyleType.CHARACTER: CharacterStyle,
    SE_StyleType.TABLE: TableStyle,
    SE_StyleType.NUMBERING: NumberingStyle,
    None: BaseStyle,
}
