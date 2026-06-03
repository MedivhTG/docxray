from __future__ import annotations

from functools import cached_property
from typing import Any, Literal, TypedDict, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.oxml.trans.enums import (
    _SE_BORDER_TO_ECMA_NUMBER,
    _SE_BORDER_TO_LINES_COUNT,
    WD_CNF_FORMAT,
)
from docxray.oxml.trans.proxy.compute import width
from docxray.oxml.trans.proxy.shared import (
    Length,
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import TableStyle
from docxray.oxml.trans.proxy.table import Cell, Row, Table
from docxray.oxml.trans.shared import CT_TblWidth
from docxray.oxml.trans.st.enums import (
    SE_TEXT_DIRECTION,
    SE_VERTICAL_JC,
    SE_BORDER,
    SE_TblStyleOverrideType,
)
from docxray.oxml.trans.styles import CT_TblStylePr
from docxray.oxml.trans.table.cell_props import CT_TcBorders, CT_TcMar
from docxray.oxml.trans.table.table_props import CT_TblBorders

from .exceptions import DisplayError
from .how2display import How2Display
from .border import Border

type _Border = Literal["top", "bottom", "left", "right", "insideH", "insideV"]
type _TableChild = Literal["row", "cell"]

TBL_POSITIONING: dict[POS, dict[_TableChild, tuple[_Border, _Border]]] = {
    POS.ONE_ITEM: {
        "row": ("top", "bottom"),
        "cell": ("left", "right"),
    },
    POS.START: {
        "row": ("top", "insideH"),
        "cell": ("left", "insideV"),
    },
    POS.MIDDLE: {
        "row": ("insideH", "insideH"),
        "cell": ("insideV", "insideV"),
    },
    POS.END: {
        "row": ("insideH", "bottom"),
        "cell": ("insideV", "right"),
    },
}
_G = SE_TblStyleOverrideType
HORZ_GROUP = {
    _G.HEADER_ROW,
    _G.FOOTER_ROW,
    _G.HORIZONTAL_BAND_ODD,
    _G.HORIZONTAL_BAND_EVEN,
}
VERT_GROUP = {
    _G.FIRST_COLUMN,
    _G.LAST_COLUMN,
    _G.VERTICAL_BAND_ODD,
    _G.VERTICAL_BAND_EVEN,
}
CORNER_GROUP = {
    _G.TOP_LEFT_CORNER_CELL,
    _G.TOP_RIGHT_CORNER_CELL,
    _G.BOTTOM_LEFT_CORNER_CELL,
    _G.BOTTOM_RIGHT_CORNER_CELL,
}


class BordersDropped(TypedDict):
    top: bool
    bottom: bool
    left: bool
    right: bool


class BordersInfo(TypedDict):
    top: Border | None
    bottom: Border | None
    left: Border | None
    right: Border | None
    spacing: Length | float | None
    _sides_dropped_to_table_borders: BordersDropped


class PaddingInfo(TypedDict):
    top: Length | float | None
    bottom: Length | float | None
    left: Length | float | None
    right: Length | float | None


# TODO: borders info refac needed after
class CellH2D(How2Display[Cell]):
    @cached_property
    def row(self) -> Row:
        return self._proxy.row

    @cached_property
    def talbe(self) -> Table:
        return self.row.table

    @cached_property
    def borders_info(self) -> BordersInfo:
        spacing = self._spacing
        if spacing is not None and spacing > 0:
            return self._borders_non_zero_spacing_info
        return self._spacing_zero(self._borders_non_zero_spacing_info)

    @cached_property
    def padding_info(self) -> PaddingInfo:
        def _mar(
            mar_width: CT_TblWidth | None,
            fallbacks_width: list[CT_TblWidth | None] | None = None,
        ) -> Length | float | None:
            if mar_width is None:
                if fallbacks_width is None:
                    return None
                for fallback in fallbacks_width:
                    if fallback is not None:
                        mar_width = fallback
                        break
            if mar_width is None:
                return None
            return width(mar_width)

        padding: PaddingInfo = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
        }
        cell_mar = self._cell_mar_ctx[0]
        tbl_cell_mar = self.talbe.h2d._tblCellMar
        if cell_mar is None and tbl_cell_mar is None:
            pass
        elif cell_mar is None and tbl_cell_mar is not None:
            padding["top"] = _mar(tbl_cell_mar.top)
            padding["bottom"] = _mar(tbl_cell_mar.bottom)
            padding["left"] = _mar(tbl_cell_mar.left, [tbl_cell_mar.start])
            padding["right"] = _mar(tbl_cell_mar.right, [tbl_cell_mar.end])
        elif cell_mar is not None and tbl_cell_mar is None:
            padding["top"] = _mar(cell_mar.top)
            padding["bottom"] = _mar(cell_mar.bottom)
            padding["left"] = _mar(cell_mar.left, [cell_mar.start])
            padding["right"] = _mar(cell_mar.right, [cell_mar.end])
        elif cell_mar is not None and tbl_cell_mar is not None:
            padding["top"] = _mar(cell_mar.top, [tbl_cell_mar.top])
            padding["bottom"] = _mar(cell_mar.bottom, [tbl_cell_mar.bottom])
            padding["left"] = _mar(
                cell_mar.left,
                [cell_mar.start, tbl_cell_mar.left, tbl_cell_mar.start],
            )
            padding["right"] = _mar(
                cell_mar.right,
                [cell_mar.right, tbl_cell_mar.right, tbl_cell_mar.end],
            )
        return padding

    # TODO: inherit from parent Section if omitted
    @cached_property
    def content_flow(self) -> SE_TEXT_DIRECTION | None:
        text_flow = self._prop_val("textDirection", algorithm="both")
        if not isinstance(text_flow, NotFound):
            return text_flow
        return None

    @cached_property
    def vertical_align(self) -> SE_VERTICAL_JC:
        align = self._prop_val("vAlign", algorithm="both")
        if not isinstance(align, NotFound):
            return align
        return SE_VERTICAL_JC.TOP

    @cached_property
    def _cell_mar_ctx(
        self,
    ) -> tuple[CT_TcMar | None, TableStyle | CT_TblStylePr | None]:
        return self._prop_with_ctx("tcMar")

    @cached_property
    def _table_style(self) -> TableStyle | None:
        return self.row.h2d._table_style

    @cached_property
    def _borders_non_zero_spacing_info(self) -> BordersInfo:
        inf = self._spacing_non_zero()
        inf["spacing"] = self._spacing
        return inf

    @cached_property
    def _cell_borders_ctx(
        self,
    ) -> tuple[CT_TcBorders | None, TableStyle | CT_TblStylePr | None]:
        return self._prop_with_ctx("tcBorders")

    @cached_property
    def _spacing(self) -> Length | float | None:
        name = "tblCellSpacing"
        row_h2d = self.row.h2d
        tbl_h2d = row_h2d.table.h2d
        # Row-level direct
        spacing_elm = row_h2d._prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        # Row-level exception
        tblPrEx_elm = row_h2d._tblPrEx
        if tblPrEx_elm is not None:
            spacing_elm = tblPrEx_elm.tblCellSpacing
            if spacing_elm is not None:
                return width(spacing_elm, True)
        # Table-level
        spacing_elm = tbl_h2d._prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)

        # From table style (defined common or exception)
        path = row_h2d._prop_path(name, row_h2d._path_base)
        # Table style Row-level (in grid group or direct) firstly
        spacing_elm, _ = self._from_tbl_style_hierarchy(
            self._tbl_style_props_deep, path
        )
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        # Table style Table-level (in grid group or direct) lastly
        path = tbl_h2d._prop_path(name, tbl_h2d._path_base)
        spacing_elm, _ = self._from_tbl_style_hierarchy(
            self._tbl_style_props_deep, path
        )
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        return None

    @cached_property
    def _row_band_number(self) -> int:
        cell = self._proxy
        band_shift = 1 if cell.row.h2d._shift_horz_bands else 0
        y_shift = cell.grid_y + 1 + band_shift
        return y_shift // cell.table.h2d._row_band_size

    @cached_property
    def _col_band_number(self) -> int:
        cell = self._proxy
        band_shift = 1 if cell.row.h2d._shift_vert_bands else 0
        x_shift = cell.idx + 1 + band_shift
        return x_shift // cell.table.h2d._col_band_size

    @cached_property
    def _cnf_latent(self) -> WD_CNF_FORMAT:
        _CNF = WD_CNF_FORMAT
        cell = self._proxy
        row_h2d = cell.row.h2d
        cnf = _CNF(0)
        # Special rows/columns
        if cell.grid_y == 0:
            cnf |= _CNF.FIRST_ROW
        if cell.cell_below is None:
            cnf |= _CNF.LAST_ROW
        if cell.grid_x == 0:
            cnf |= _CNF.FIRST_COLUMN
        if cell.cell_next is None:
            cnf |= _CNF.LAST_COLUMN
        # Corner group
        if cell.grid_y == 0 and cell.grid_x == 0:
            cnf |= _CNF.FIRST_ROW_LAST_COLUMN
        if cell.grid_y == 0 and cell.cell_next is None:
            cnf |= _CNF.FIRST_ROW_LAST_COLUMN
        if cell.cell_below is None and cell.grid_x == 0:
            cnf |= _CNF.LAST_ROW_FIRST_COLUMN
        if cell.cell_below is None and cell.cell_next is None:
            cnf |= _CNF.LAST_ROW_LAST_COLUMN
        # Horizontal/Vertical Bands
        has_vert_band_shift_group = (
            _CNF.FIRST_COLUMN & cnf
            or _CNF.FIRST_ROW_FIRST_COLUMN & cnf
            or _CNF.LAST_ROW_FIRST_COLUMN & cnf
        )
        if not (row_h2d._shift_vert_bands and has_vert_band_shift_group):
            if self._col_band_number % 2 == 0:
                cnf |= _CNF.EVEN_VERTICAL_BAND
            else:
                cnf |= _CNF.ODD_VERTICAL_BAND
        has_horz_band_shift_group = (
            _CNF.FIRST_ROW & cnf
            or _CNF.FIRST_ROW_FIRST_COLUMN & cnf
            or _CNF.FIRST_ROW_LAST_COLUMN & cnf
        )
        if not (row_h2d._shift_vert_bands and has_horz_band_shift_group):
            if self._row_band_number % 2 == 0:
                cnf |= _CNF.EVEN_HORIZONTAL_BAND
            else:
                cnf |= _CNF.ODD_HORIZONTAL_BAND
        return cnf

    @cached_property
    def _tbl_style_props_deep(
        self,
    ) -> list[tuple[TableStyle, list[CT_TblStylePr]]]:
        tbl_style = self._table_style
        props_leveled = []
        cnf = self._cnf_latent
        while isinstance(tbl_style, TableStyle):
            if cnf is not None:
                tbl_style_props = self._table_style_props(tbl_style, cnf)
            else:
                tbl_style_props = []
            props_leveled.append((tbl_style, tbl_style_props))
            tbl_style = self._styles.base_style(tbl_style)  # type: ignore[assignment]
        return props_leveled

    def _spacing_non_zero(self) -> BordersInfo:
        inf: BordersInfo = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "spacing": None,
            "_sides_dropped_to_table_borders": {
                "top": False,
                "bottom": False,
                "left": False,
                "right": False,
            },
        }
        tcBorders_elm, cell_ctx = self._cell_borders_ctx
        tblBorders_elm = self.row.h2d._tblBorders
        tbl_horz = self._border(tblBorders_elm, "insideH")
        tbl_vert = self._border(tblBorders_elm, "insideV")
        if tcBorders_elm is None and cell_ctx is None:
            self._case_1_tc_borders_ommited(inf, tbl_horz, tbl_vert)
        if tcBorders_elm is not None and cell_ctx is None:
            self._case_2_tc_borders_direct(
                inf, tcBorders_elm, tbl_horz, tbl_vert
            )
        if tcBorders_elm is not None and isinstance(cell_ctx, TableStyle):
            self._case_3_tc_borders_style_direct(
                inf, tcBorders_elm, tbl_horz, tbl_vert
            )
        if tcBorders_elm is not None and isinstance(cell_ctx, CT_TblStylePr):
            self._case_4_tc_borders_grid_group(
                inf, tcBorders_elm, tbl_horz, tbl_vert, cell_ctx.type
            )
        return inf

    def _spacing_zero(self, inf: BordersInfo) -> BordersInfo:
        # Drop and compute again
        dropped = inf["_sides_dropped_to_table_borders"]
        if dropped["top"]:
            inf["top"] = None
        if dropped["bottom"]:
            inf["bottom"] = None
        if dropped["left"]:
            inf["left"] = None
        if dropped["right"]:
            inf["right"] = None

        cell = self._proxy
        row = cell.row
        tblBorders_elm = self.row.h2d._tblBorders

        cell_above = cell.cell_above
        cell_above_h2d = cell_above.h2d if cell_above is not None else None
        cell_below = cell.cell_below
        cell_below_h2d = cell_below.h2d if cell_below is not None else None
        cell_prev = cell.cell_prev
        cell_prev_h2d = cell_prev.h2d if cell_prev is not None else None
        cell_next = cell.cell_next
        cell_next_h2d = cell_next.h2d if cell_next is not None else None

        tbl_top = self._border(tblBorders_elm, "top")
        tbl_bottom = self._border(tblBorders_elm, "bottom")
        tbl_left = self._border(tblBorders_elm, "left")
        tbl_right = self._border(tblBorders_elm, "right")
        tbl_horz = self._border(tblBorders_elm, "insideH")
        tbl_vert = self._border(tblBorders_elm, "insideV")

        self._vert_borders_conflict(
            inf,
            cell.pos,
            cell_prev_h2d,
            cell_next_h2d,
            tbl_left,
            tbl_right,
            tbl_vert,
        )
        self._horz_borders_conflict(
            inf,
            row.pos,
            cell_above_h2d,
            cell_below_h2d,
            tbl_top,
            tbl_bottom,
            tbl_horz,
        )

        return inf

    def _case_1_tc_borders_ommited(
        self,
        inf: BordersInfo,
        tbl_horz: Border | None,
        tbl_vert: Border | None,
    ) -> None:
        inf["top"] = tbl_horz
        inf["bottom"] = tbl_horz
        inf["left"] = tbl_vert
        inf["right"] = tbl_vert

    def _case_2_tc_borders_direct(
        self,
        inf: BordersInfo,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: Border | None,
        tbl_vert: Border | None,
    ) -> None:
        top = self._border(tcBorders_elm, "top")
        if top:
            inf["top"] = top
        else:
            inf["_sides_dropped_to_table_borders"]["top"] = True
            inf["top"] = tbl_horz
        bottom = self._border(tcBorders_elm, "bottom")
        if bottom:
            inf["bottom"] = bottom
        else:
            inf["_sides_dropped_to_table_borders"]["bottom"] = True
            inf["bottom"] = tbl_horz
        left = self._border(tcBorders_elm, "left")
        if left:
            inf["left"] = left
        else:
            inf["_sides_dropped_to_table_borders"]["left"] = True
            inf["left"] = tbl_vert
        right = self._border(tcBorders_elm, "right")
        if right:
            inf["right"] = right
        else:
            inf["_sides_dropped_to_table_borders"]["right"] = True
            inf["right"] = tbl_vert

    def _case_3_tc_borders_style_direct(
        self,
        inf: BordersInfo,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: Border | None,
        tbl_vert: Border | None,
    ) -> None:
        self._case_2_tc_borders_direct(inf, tcBorders_elm, tbl_horz, tbl_vert)

    def _case_4_tc_borders_grid_group(
        self,
        inf: BordersInfo,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: Border | None,
        tbl_vert: Border | None,
        grid_group: SE_TblStyleOverrideType,
    ) -> None:
        cell = self._proxy
        row = cell.row
        top = None
        bottom = None
        left = None
        right = None
        if grid_group == SE_TblStyleOverrideType.ENTIRE_TABLE:
            top, bottom = self._choose_horz(
                inf["_sides_dropped_to_table_borders"],
                row.pos,
                tcBorders_elm,
                tbl_horz,
            )
            left, right = self._choose_vert(
                inf["_sides_dropped_to_table_borders"],
                cell.pos,
                tcBorders_elm,
                tbl_vert,
            )
        elif grid_group in HORZ_GROUP:
            top, bottom = self._choose_horz(
                inf["_sides_dropped_to_table_borders"],
                POS.ONE_ITEM,
                tcBorders_elm,
                tbl_horz,
            )
            left, right = self._choose_vert(
                inf["_sides_dropped_to_table_borders"],
                cell.pos,
                tcBorders_elm,
                tbl_vert,
            )
        elif grid_group in VERT_GROUP:
            top, bottom = self._choose_horz(
                inf["_sides_dropped_to_table_borders"],
                row.pos,
                tcBorders_elm,
                tbl_horz,
            )
            left, right = self._choose_vert(
                inf["_sides_dropped_to_table_borders"],
                POS.ONE_ITEM,
                tcBorders_elm,
                tbl_vert,
            )
        elif grid_group in CORNER_GROUP:
            top, bottom = self._choose_horz(
                inf["_sides_dropped_to_table_borders"],
                POS.ONE_ITEM,
                tcBorders_elm,
                tbl_horz,
            )
            left, right = self._choose_vert(
                inf["_sides_dropped_to_table_borders"],
                POS.ONE_ITEM,
                tcBorders_elm,
                tbl_vert,
            )
        inf["top"] = top
        inf["bottom"] = bottom
        inf["left"] = left
        inf["right"] = right

    def _choose_horz(
        self,
        dropped: BordersDropped,
        row_pos: POS,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: Border | None,
    ) -> tuple[Border | None, Border | None]:
        top_n, bottom_n = TBL_POSITIONING[row_pos]["row"]
        top = self._border(tcBorders_elm, top_n)
        if top_n == "insideH" and top is None:
            top_got = self._border(tcBorders_elm, "top")
            if top_got:
                top = top_got
            else:
                dropped["top"] = True
                top = tbl_horz
        bottom = self._border(tcBorders_elm, bottom_n)
        if bottom_n == "insideH" and bottom is None:
            bottom_got = self._border(tcBorders_elm, "bottom")
            if bottom_got:
                bottom = bottom_got
            else:
                dropped["bottom"] = True
                bottom = tbl_horz
        return top, bottom

    def _choose_vert(
        self,
        dropped: BordersDropped,
        cell_pos: POS,
        tcBorders_elm: CT_TcBorders,
        tbl_vert: Border | None,
    ) -> tuple[Border | None, Border | None]:
        left_n, right_n = TBL_POSITIONING[cell_pos]["cell"]
        left = self._border(tcBorders_elm, left_n)
        if left_n == "insideV" and left is None:
            left_got = self._border(tcBorders_elm, "left")
            if left_got:
                left = left_got
            else:
                dropped["left"] = True
                left = tbl_vert
        right = self._border(tcBorders_elm, right_n)
        if right_n == "insideV" and right is None:
            right_got = self._border(tcBorders_elm, "right")
            if right_got:
                right = right_got
            else:
                dropped["right"] = True
                right = tbl_vert
        return left, right

    def _border(
        self, borders_elm: CT_TcBorders | CT_TblBorders | None, border: _Border
    ) -> Border | None:
        path = self._prop_path(border)
        prop = safe_get_prop(borders_elm, path)
        if isinstance(prop, NotFound):
            return None
        return Border(prop, self._proxy)

    def _vert_borders_conflict(
        self,
        inf: BordersInfo,
        cell_pos: POS,
        cell_prev_h2d: CellH2D | None,
        cell_next_h2d: CellH2D | None,
        tbl_left: Border | None,
        tbl_right: Border | None,
        tbl_vert: Border | None,
    ) -> None:
        left_n, right_n = TBL_POSITIONING[cell_pos]["cell"]
        if left_n == "left":
            inf["left"] = self._opposing_cell_borders_conflict(
                inf["left"], tbl_left, True
            )
        elif left_n == "insideV" and cell_prev_h2d is not None:
            prev_inf = cell_prev_h2d._borders_non_zero_spacing_info
            right_dropped = prev_inf["_sides_dropped_to_table_borders"][
                "right"
            ]
            if prev_inf["right"]:
                inf["left"] = self._opposing_cell_borders_conflict(
                    inf["left"], prev_inf["right"], right_dropped
                )
            else:
                inf["left"] = self._opposing_cell_borders_conflict(
                    inf["left"], tbl_vert, True
                )
        if right_n == "right":
            inf["right"] = self._opposing_cell_borders_conflict(
                inf["right"], tbl_right, True
            )
        elif right_n == "insideV" and cell_next_h2d is not None:
            next_inf = cell_next_h2d._borders_non_zero_spacing_info
            left_dropped = next_inf["_sides_dropped_to_table_borders"]["left"]
            if next_inf["right"]:
                inf["right"] = self._opposing_cell_borders_conflict(
                    inf["right"], next_inf["left"], left_dropped
                )
            else:
                inf["right"] = self._opposing_cell_borders_conflict(
                    inf["right"], tbl_vert, True
                )

    def _horz_borders_conflict(
        self,
        inf: BordersInfo,
        row_pos: POS,
        cell_above_h2d: CellH2D | None,
        cell_below_h2d: CellH2D | None,
        tbl_top: Border | None,
        tbl_bottom: Border | None,
        tbl_horz: Border | None,
    ) -> None:
        top_n, bottom_n = TBL_POSITIONING[row_pos]["row"]
        if top_n == "top":
            inf["top"] = self._opposing_cell_borders_conflict(
                inf["top"], tbl_top, True
            )
        elif top_n == "insideH" and cell_above_h2d is not None:
            above_inf = cell_above_h2d._borders_non_zero_spacing_info
            bottom_dropped = above_inf["_sides_dropped_to_table_borders"][
                "bottom"
            ]
            if above_inf["bottom"]:
                inf["top"] = self._opposing_cell_borders_conflict(
                    inf["top"], above_inf["bottom"], bottom_dropped
                )
            else:
                inf["top"] = self._opposing_cell_borders_conflict(
                    inf["top"], tbl_horz, True
                )
        if bottom_n == "bottom":
            inf["bottom"] = self._opposing_cell_borders_conflict(
                inf["bottom"], tbl_bottom, True
            )
        elif bottom_n == "insideH" and cell_below_h2d is not None:
            below_inf = cell_below_h2d._borders_non_zero_spacing_info
            bottom_dropped = below_inf["_sides_dropped_to_table_borders"][
                "top"
            ]
            if below_inf["top"]:
                inf["bottom"] = self._opposing_cell_borders_conflict(
                    inf["bottom"], below_inf["top"]
                )
            else:
                inf["bottom"] = self._opposing_cell_borders_conflict(
                    inf["bottom"], tbl_horz, True
                )

    def _opposing_cell_borders_conflict(
        self,
        main: Border | None,
        opposing_to: Border | None,
        opposed_to_table: bool = False,
    ) -> Border | None:
        none = (None, SE_BORDER.NULL, SE_BORDER.NONE)
        if opposed_to_table:
            if main is None or main.border_type is None:
                return opposing_to
            else:
                return main
        else:
            if main is None:
                return opposing_to
            elif main.border_type in none:
                return opposing_to
            elif opposing_to is None:
                return main
            elif opposing_to.border_type in none:
                return main
        main = cast("Border", main)
        opposing_to = cast("Border", opposing_to)
        main_weight = self._border_weight(main.border_type)
        opposing_to_weight = self._border_weight(opposing_to.border_type)
        if main_weight is None or opposing_to_weight is None:
            msg = "Art borders detected in table of story part"
            raise DisplayError(msg)
        if main_weight > opposing_to_weight:
            return main
        elif main_weight < opposing_to_weight:
            return opposing_to
        elif main_weight == opposing_to_weight:
            main_number = _SE_BORDER_TO_ECMA_NUMBER[main.border_type]
            opposing_to_number = _SE_BORDER_TO_ECMA_NUMBER[
                opposing_to.border_type
            ]
            if main_number <= opposing_to_number:
                return main
            return opposing_to
        return None

    def _border_weight(self, border_type: SE_BORDER) -> int | None:
        lines_count = _SE_BORDER_TO_LINES_COUNT.get(border_type)
        border_number = _SE_BORDER_TO_ECMA_NUMBER.get(border_type)
        if lines_count is None or border_number is None:
            # It's an art border
            return None
        return lines_count * border_number

    def _prop_with_ctx(
        self, name: str
    ) -> tuple[Any | None, TableStyle | CT_TblStylePr | None]:
        tcBorders_elm = self._prop(name)
        if not isinstance(tcBorders_elm, NotFound):
            return tcBorders_elm, None
        path = self._prop_path(name, self._path_base)
        tc_ctx = self._from_tbl_style_hierarchy(
            self._tbl_style_props_deep, path
        )
        if not isinstance(tc_ctx[0], NotFound):
            return tc_ctx
        return None, None

    def _cnf_looked(self, cnf: WD_CNF_FORMAT) -> WD_CNF_FORMAT:
        row_h2d = self.row.h2d
        if not row_h2d.first_row_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
        if not row_h2d.last_row_show:
            cnf &= ~WD_CNF_FORMAT.LAST_ROW
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if not row_h2d.first_col_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
        if not row_h2d.last_col_show:
            cnf &= ~WD_CNF_FORMAT.LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if row_h2d.no_horizontal_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_HORIZONTAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND
        if row_h2d.no_vertical_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_VERTICAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_VERTICAL_BAND
        return cnf

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._table_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._table_style, path, optional)
