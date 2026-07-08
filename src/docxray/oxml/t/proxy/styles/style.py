"""Style object hierarchy."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.oxml.t.enums import WD_CNF_FORMAT
from docxray.oxml.t.proxy.base import ElementProxy, NotFound
from docxray.oxml.t.st.enums import SE_STYLE_TYPE, SE_TBL_STYLE_OVERRIDE_TYPE
from docxray.oxml.t.styles import CT_Style, CT_Styles, CT_TblStylePr

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.parts.styles import StylesPart
    from docxray.oxml.t.proxy.numbering.numbering import Num, Numbering


def StyleFactory(style_elm: CT_Style, part: StylesPart) -> BaseStyle:
    """Return `Style` object of appropriate |BaseStyle| subclass for `style_elm`."""
    return S_TYPE_TO_STYLE_CLS[style_elm.type](style_elm, part)


class BaseStyle(ElementProxy[CT_Style]):
    @cached_property
    def part(self) -> StylesPart:
        return cast("StylesPart", self._parent)

    @cached_property
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
        return self.tbl_style_prop(SE_TBL_STYLE_OVERRIDE_TYPE.ENTIRE_TABLE)

    @cached_property
    def firstRow(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TBL_STYLE_OVERRIDE_TYPE.HEADER_ROW)

    @cached_property
    def lastRow(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TBL_STYLE_OVERRIDE_TYPE.FOOTER_ROW)

    @cached_property
    def firstCol(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TBL_STYLE_OVERRIDE_TYPE.FIRST_COLUMN)

    @cached_property
    def lastCol(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(SE_TBL_STYLE_OVERRIDE_TYPE.LAST_COLUMN)

    @cached_property
    def band1Vert(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.VERTICAL_BAND_ODD
        )

    @cached_property
    def band2Vert(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.VERTICAL_BAND_EVEN
        )

    @cached_property
    def band1Horz(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.HORIZONTAL_BAND_ODD
        )

    @cached_property
    def band2Horz(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.HORIZONTAL_BAND_EVEN
        )

    @cached_property
    def nwCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.TOP_LEFT_CORNER_CELL
        )

    @cached_property
    def neCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.TOP_RIGHT_CORNER_CELL
        )

    @cached_property
    def swCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.BOTTOM_LEFT_CORNER_CELL
        )

    @cached_property
    def seCell(self) -> CT_TblStylePr | None:
        return self.tbl_style_prop(
            SE_TBL_STYLE_OVERRIDE_TYPE.BOTTOM_RIGHT_CORNER_CELL
        )

    def bitwise_tbl_style_prop(
        self, flag: WD_CNF_FORMAT
    ) -> CT_TblStylePr | None:
        return getattr(self, flag.format_name(), None)

    def tbl_style_prop(
        self, type: SE_TBL_STYLE_OVERRIDE_TYPE
    ) -> CT_TblStylePr | None:
        return self.element.tblStylePr_for(type)

    def table_style_props(self, cnf: WD_CNF_FORMAT) -> list[CT_TblStylePr]:
        """Get desired table style properties from given tables using an cnf bit mask.

        Args:
            table_style (TableStyle): Given table style
            cnf (WD_CNF_FORMAT): Fiven conditional formatting for table (CNF) bit mask.

        Returns:
            list[CT_TblStylePr]: List of table style properties.
        """
        props = []
        for flag in WD_CNF_FORMAT.ordered_flags():
            format = cnf & flag
            if format:
                tblStylePr_elm = self.bitwise_tbl_style_prop(flag)
                if tblStylePr_elm is not None:
                    props.append(tblStylePr_elm)
        if self.wholeTable:
            props.append(self.wholeTable)
        return props


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
        num_id = self.prop("pPr.numPr.numId.val")
        if isinstance(num_id, NotFound):
            raise err
        return self.numbering.get_num(num_id)


S_TYPE_TO_STYLE_CLS: dict[SE_STYLE_TYPE | None, Any] = {
    SE_STYLE_TYPE.PARAGRAPH: ParagraphStyle,
    SE_STYLE_TYPE.CHARACTER: CharacterStyle,
    SE_STYLE_TYPE.TABLE: TableStyle,
    SE_STYLE_TYPE.NUMBERING: NumberingStyle,
    None: BaseStyle,
}
