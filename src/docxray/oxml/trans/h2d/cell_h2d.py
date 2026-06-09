from __future__ import annotations

from functools import cached_property
from typing import Any, Literal, TypedDict, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.oxml.trans.enums import (
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
    SE_BORDER,
    SE_TEXT_DIRECTION,
    SE_VERTICAL_JC,
    SE_TblStyleOverrideType,
)
from docxray.oxml.trans.styles import CT_TblStylePr
from docxray.oxml.trans.table.cell_props import CT_TcMar

from .border import Border
from .how2display import How2Display

type _Border = Literal["top", "bottom", "left", "right", "insideH", "insideV"]
type _Side = Literal["top", "bottom", "left", "right"]
type _TableChild = Literal["row", "cell"]
type _BorderCtx = tuple[Border, None | TableStyle | CT_TblStylePr] | None

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


class PaddingInfo(TypedDict):
    top: Length | float | None
    bottom: Length | float | None
    left: Length | float | None
    right: Length | float | None


class CellH2D(How2Display[Cell]):
    @cached_property
    def row(self) -> Row:
        return self._proxy.row

    @cached_property
    def table(self) -> Table:
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
        tbl_cell_mar = self.row.h2d._tblCellMar
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
    def _spacing(self) -> Length | float | None:
        name = "tblCellSpacing"
        row_h2d = self.row.h2d
        tbl_h2d = row_h2d.table.h2d
        # Row-level direct
        spacing_elm = row_h2d._prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        # Row-level exception or Table-level direct
        spacing_elm = row_h2d._tblCellSpacing
        if spacing_elm is not None:
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
            cnf |= _CNF.FIRST_ROW_FIRST_COLUMN
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
    def _cnf_looked(self) -> WD_CNF_FORMAT:
        row_h2d = self.row.h2d
        cnf = self._cnf_latent
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

    @cached_property
    def _self_top(self) -> _BorderCtx:
        return self._self_border("top")

    @cached_property
    def _self_bottom(self) -> _BorderCtx:
        return self._self_border("bottom")

    @cached_property
    def _self_left(self) -> _BorderCtx:
        return self._self_border("left")

    @cached_property
    def _self_right(self) -> _BorderCtx:
        return self._self_border("right")

    @cached_property
    def _self_insideH(self) -> _BorderCtx:
        return self._self_border("insideH")

    @cached_property
    def _self_insideV(self) -> _BorderCtx:
        return self._self_border("insideV")

    @cached_property
    def _tbl_style_props_deep(
        self,
    ) -> list[tuple[TableStyle, list[CT_TblStylePr]]]:
        tbl_style = self._table_style
        props_leveled = []
        cnf = self._cnf_looked
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
        }
        sides = ["top", "bottom", "left", "right"]
        for side_n in sides:
            self._choose_side(inf, cast("_Side", side_n))
        return inf

    # TODO: here can be bugs with grid groups
    def _spacing_zero(self, inf: BordersInfo) -> BordersInfo:
        # Drop and compute again
        self._vert_borders_conflict(inf)
        self._horz_borders_conflict(inf)
        return inf

    # TODO: known bug - horizontals bands in WORD overriden idk why (or other grid groups)
    def _choose_side(self, inf: BordersInfo, side_n: _Side) -> None:
        row_h2d = self.row.h2d
        if side_n in ("top", "bottom"):
            cell_inside_ctx = self._self_insideH
            table_inside = row_h2d._table_insideH
            inside_n = "insideH"
            tbl_child = "row"
            one_item_group = HORZ_GROUP | CORNER_GROUP
        else:
            cell_inside_ctx = self._self_insideV
            table_inside = row_h2d._table_insideV
            inside_n = "insideV"
            tbl_child = "cell"
            one_item_group = VERT_GROUP | CORNER_GROUP
        if side_n in ("top", "left"):
            take_first = True
        else:
            take_first = False
        init_pos = self.row.pos if tbl_child == "row" else self._proxy.pos

        def _side_on_ctx(
            border_ctx: _BorderCtx, desired_n: str
        ) -> Border | None:
            nonlocal init_pos, take_first, tbl_child

            pos = init_pos
            if border_ctx is None:
                return None
            side_got, ctx = border_ctx
            # Always get self-cell borders
            if ctx is None or isinstance(ctx, TableStyle):
                pos = POS.ONE_ITEM
            # No meaning in ctx for insides
            elif isinstance(ctx, CT_TblStylePr) and ctx.type in one_item_group:
                pos = POS.ONE_ITEM
            first_n, second_n = TBL_POSITIONING[pos][
                cast("_TableChild", tbl_child)
            ]
            # Top or bottom, left or right
            preferred_n = first_n if take_first else second_n
            if preferred_n == desired_n:
                return side_got
            return None

        side = None
        side_ctx: _BorderCtx = getattr(self, f"_self_{side_n}")
        # If no side context - look for inside border
        if side_ctx is None:
            side = _side_on_ctx(cell_inside_ctx, inside_n)
        # Else resolve between sides
        else:
            side = _side_on_ctx(side_ctx, side_n)
            if side is None:
                side = _side_on_ctx(cell_inside_ctx, inside_n)
        # If None we got even now - go for table side
        # TODO: for safety.. but render bugs
        if side is None and table_inside is not None:
            side = table_inside
        inf[side_n] = side

    def _self_border(self, border: _Border) -> _BorderCtx:
        path = PropertyPath.base(border, "tcPr.tcBorders")
        border_elm = self._prop(path)
        if not isinstance(border_elm, NotFound):
            return Border(border_elm, self._proxy), None
        for tbl_style, tbl_style_props in self._tbl_style_props_deep:
            if not tbl_style_props:
                border_elm = safe_get_prop(tbl_style.element, path, False)
                if not isinstance(border_elm, NotFound):
                    return Border(border_elm, self._proxy), tbl_style
            else:
                for prop in tbl_style_props:
                    border_elm = safe_get_prop(prop, path, False)
                    if not isinstance(border_elm, NotFound):
                        return Border(border_elm, self._proxy), prop
        return None

    def _vert_borders_conflict(self, inf: BordersInfo) -> None:
        cell = self._proxy
        row_h2d = self.row.h2d
        tbl_left = row_h2d._table_left
        tbl_right = row_h2d._table_right
        tbl_vert = row_h2d._table_insideV
        cell_prev = cell.cell_prev
        cell_prev_h2d = cell_prev.h2d if cell_prev is not None else None
        cell_next = cell.cell_next
        cell_next_h2d = cell_next.h2d if cell_next is not None else None
        left_n, right_n = TBL_POSITIONING[cell.pos]["cell"]
        if left_n == "left":
            inf["left"] = Border.oppose(inf["left"], tbl_left)
        elif left_n == "insideV" and cell_prev_h2d is not None:
            prev_inf = cell_prev_h2d._borders_non_zero_spacing_info
            inf["left"] = Border.oppose(
                inf["left"], prev_inf["right"] or tbl_vert
            )
        if right_n == "right":
            inf["right"] = Border.oppose(inf["right"], tbl_right)
        elif right_n == "insideV" and cell_next_h2d is not None:
            next_inf = cell_next_h2d._borders_non_zero_spacing_info
            inf["right"] = Border.oppose(
                inf["right"], next_inf["left"] or tbl_vert
            )

    def _horz_borders_conflict(self, inf: BordersInfo) -> None:
        cell = self._proxy
        row_h2d = self.row.h2d
        tbl_top = row_h2d._table_top
        tbl_bottom = row_h2d._table_bottom
        tbl_horz = row_h2d._table_insideH
        cell_above = cell.cell_above
        cell_above_h2d = cell_above.h2d if cell_above is not None else None
        cell_below = cell.cell_below
        cell_below_h2d = cell_below.h2d if cell_below is not None else None
        top_n, bottom_n = TBL_POSITIONING[self.row.pos]["row"]

        if top_n == "top":
            inf["top"] = Border.oppose(inf["top"], tbl_top)
        elif top_n == "insideH" and cell_above_h2d is not None:
            above_inf = cell_above_h2d._borders_non_zero_spacing_info
            inf["top"] = Border.oppose(
                inf["top"], above_inf["bottom"] or tbl_horz
            )
        if bottom_n == "bottom":
            inf["bottom"] = Border.oppose(inf["bottom"], tbl_bottom)
        elif bottom_n == "insideH" and cell_below_h2d is not None:
            below_inf = cell_below_h2d._borders_non_zero_spacing_info
            inf["bottom"] = Border.oppose(
                inf["bottom"], below_inf["top"] or tbl_horz
            )

    def _prop_with_ctx(
        self, name: str
    ) -> tuple[Any | None, TableStyle | CT_TblStylePr | None]:
        elm = self._prop(name)
        if not isinstance(elm, NotFound):
            return elm, None
        path = self._prop_path(name, self._path_base)
        tc_ctx = self._from_tbl_style_hierarchy(
            self._tbl_style_props_deep, path
        )
        if not isinstance(tc_ctx[0], NotFound):
            return tc_ctx
        return None, None

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._table_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._table_style, path, optional)
