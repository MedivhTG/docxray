from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, TypedDict, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.length import Length
from docxray.oxml.t.enums import WD_CNF_FORMAT
from docxray.oxml.t.proxy.base import (
    NotFound,
    PropertyPath,
    from_style_inheritance,
    safe_get_prop,
)
from docxray.oxml.t.proxy.blkcntnr import BlockItemContainer
from docxray.oxml.t.proxy.border import Border
from docxray.oxml.t.proxy.compute import width
from docxray.oxml.t.proxy.styles.style import TableStyle
from docxray.oxml.t.shared import CT_TblWidth
from docxray.oxml.t.st.enums import (
    SE_MERGE,
    SE_TBL_STYLE_OVERRIDE_TYPE,
    SE_TEXT_DIRECTION,
    SE_VERTICAL_JC,
)
from docxray.oxml.t.styles import CT_TblStylePr
from docxray.oxml.t.table.cell_props import CT_TcBorders, CT_TcMar
from docxray.oxml.t.table.table import CT_Tc

if TYPE_CHECKING:
    from .row import Row
    from .table import Table

type _Border = Literal["top", "bottom", "left", "right", "insideH", "insideV"]
type _Side = Literal["top", "bottom", "left", "right"]
type _TableChild = Literal["row", "cell"]
type _BorderCtx = tuple[Border, None | TableStyle | CT_TblStylePr] | None

_G = SE_TBL_STYLE_OVERRIDE_TYPE
_HORZ_GROUP = {
    _G.HEADER_ROW,
    _G.FOOTER_ROW,
    _G.HORIZONTAL_BAND_ODD,
    _G.HORIZONTAL_BAND_EVEN,
}
_VERT_GROUP = {
    _G.FIRST_COLUMN,
    _G.LAST_COLUMN,
    _G.VERTICAL_BAND_ODD,
    _G.VERTICAL_BAND_EVEN,
}
_CORNER_GROUP = {
    _G.TOP_LEFT_CORNER_CELL,
    _G.TOP_RIGHT_CORNER_CELL,
    _G.BOTTOM_LEFT_CORNER_CELL,
    _G.BOTTOM_RIGHT_CORNER_CELL,
}
_TBL_POSITIONING: dict[POS, dict[_TableChild, tuple[_Border, _Border]]] = {
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


class TblPosError(Exception):
    pass


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


class CellOnBorderGrid:
    def __init__(
        self,
        cell: Cell,
        tcBorders_elm: CT_TcBorders,
        grid_group: SE_TBL_STYLE_OVERRIDE_TYPE,
    ) -> None:
        self._cell = cell
        self._tcBorders_elm = tcBorders_elm
        self._group = grid_group

    @cached_property
    def sides(
        self,
    ) -> tuple[Border | None, Border | None, Border | None, Border | None]:
        row_pos = self._cell.row.pos
        cell_pos = self._cell.pos
        if self._group in _HORZ_GROUP:
            row_pos = POS.ONE_ITEM
        elif self._group in _VERT_GROUP:
            cell_pos = POS.ONE_ITEM
        elif self._group in _CORNER_GROUP:
            row_pos = POS.ONE_ITEM
            cell_pos = POS.ONE_ITEM
        # Top, Bottom
        top_n, bottom_n = _TBL_POSITIONING[row_pos]["row"]
        top = None
        bottom = None
        # Top
        if top_n == "top":
            top_elm = getattr(self._tcBorders_elm, "top", None)
            if top_elm is not None:
                top = Border(top_elm, self._cell)
        else:
            top = self._self_insideH
            # Fallback
            if (
                top is None
                and self._group == SE_TBL_STYLE_OVERRIDE_TYPE.ENTIRE_TABLE
            ):
                top_elm = getattr(self._tcBorders_elm, "top", None)
                if top_elm is not None:
                    top = Border(top_elm, self._cell)

        # Bottom
        if bottom_n == "bottom":
            bottom_elm = getattr(self._tcBorders_elm, "bottom", None)
            if bottom_elm is not None:
                bottom = Border(bottom_elm, self._cell)
        else:
            bottom = self._self_insideH
            # Fallback
            if (
                bottom is None
                and self._group == SE_TBL_STYLE_OVERRIDE_TYPE.ENTIRE_TABLE
            ):
                bottom_elm = getattr(self._tcBorders_elm, "bottom", None)
                if bottom_elm is not None:
                    bottom = Border(bottom_elm, self._cell)
        # Left, Right
        left_n, right_n = _TBL_POSITIONING[cell_pos]["cell"]
        left = None
        right = None
        # Left
        if left_n == "left":
            left_elm = getattr(self._tcBorders_elm, "left", None)
            if left_elm is not None:
                left = Border(left_elm, self._cell)
        else:
            left = self._self_insideV
            # Fallback
            if (
                left is None
                and self._group == SE_TBL_STYLE_OVERRIDE_TYPE.ENTIRE_TABLE
            ):
                left_elm = getattr(self._tcBorders_elm, "left", None)
                if left_elm is not None:
                    left = Border(left_elm, self._cell)
        # Right
        if right_n == "right":
            right_elm = getattr(self._tcBorders_elm, "right", None)
            if right_elm is not None:
                right = Border(right_elm, self._cell)
        else:
            right = self._self_insideV
            # Fallback
            if (
                right is None
                and self._group == SE_TBL_STYLE_OVERRIDE_TYPE.ENTIRE_TABLE
            ):
                right_elm = getattr(self._tcBorders_elm, "right", None)
                if right_elm is not None:
                    right = Border(right_elm, self._cell)
        return top, bottom, left, right

    @cached_property
    def top(self) -> Border | None:
        return self.sides[0]

    @cached_property
    def bottom(self) -> Border | None:
        return self.sides[1]

    @cached_property
    def left(self) -> Border | None:
        return self.sides[2]

    @cached_property
    def right(self) -> Border | None:
        return self.sides[3]

    @cached_property
    def _self_insideH(self) -> Border | None:
        if self._group in _HORZ_GROUP | _CORNER_GROUP:
            return None
        insideH_elm = getattr(self._tcBorders_elm, "insideH", None)
        if insideH_elm is None:
            return None
        return Border(insideH_elm, self._cell)

    @cached_property
    def _self_insideV(self) -> Border | None:
        if self._group in _VERT_GROUP | _CORNER_GROUP:
            return None
        insideV_elm = getattr(self._tcBorders_elm, "insideV", None)
        if insideV_elm is None:
            return None
        return Border(insideV_elm, self._cell)


class Cell(BlockItemContainer[CT_Tc]):
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
        tbl_cell_mar = self.row._tblCellMar
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

    @cached_property
    def row(self) -> Row:
        """Current row."""
        return cast("Row", self._parent)

    @cached_property
    def table(self) -> Table:
        """Current table."""
        return self.row.table

    @cached_property
    def vertical_alignment(self) -> SE_VERTICAL_JC:
        align = self._prop("tcPr.vAlign.val", where="both")
        if isinstance(align, NotFound):
            return SE_VERTICAL_JC.TOP
        return align

    # TODO: inherit from parent Section if omitted
    @cached_property
    def content_flow(self) -> SE_TEXT_DIRECTION | None:
        flow = self._prop("tcPr.textDirection.val", where="both")
        if isinstance(flow, NotFound):
            return None
        return flow

    @cached_property
    def width(self) -> Length | float | None:
        """Cell width in twips or percents, `None` if auto."""
        tcW_elm = self._prop("tcPr.tcW")
        if isinstance(tcW_elm, NotFound) or tcW_elm is None:
            return None
        return width(tcW_elm)

    @cached_property
    def horz_span(self) -> int:
        """Horizontal span of cells number like in HTML."""
        span = self._prop("tcPr.gridSpan.val")
        if isinstance(span, NotFound):
            return 1
        return span

    @cached_property
    def idx(self) -> int:
        """Cell index in a row (in XML)."""
        return self.row.cells.index(self)

    @cached_property
    def grid_x(self) -> int:
        """Cell x-dimension (columns) index in table grid."""
        x = 0
        dflt = 1
        for i in range(self.idx):
            cell = self.row.get_cell(i)
            if cell is None:
                x += dflt
                continue
            x += cell.horz_span
        return x

    @cached_property
    def grid_y(self) -> int:
        """Cell y-dimension (rows) index in table grid."""
        return self.row.idx

    @cached_property
    def vert_merged(self) -> bool:
        """Flag if cell is vertically merged."""
        if self._vmerge in (None, SE_MERGE.CONTINUE):
            return True
        return False

    @cached_property
    def cell_above(self) -> Cell | None:
        """Cell is right on top of current in table grid. `None` if not."""
        above = self.table.get_cell_on_grid(self.grid_x, self.grid_y - 1)
        while above:
            # Skip vert merged cells to get origin reference
            if not above.vert_merged:
                return above
            above = self.table.get_cell_on_grid(self.grid_x, above.grid_y - 1)
        return None

    @cached_property
    def cell_below(self) -> Cell | None:
        """Cell is right at the bottom of current in table grid. `None` if not."""
        below = self.table.get_cell_on_grid(self.grid_x, self.grid_y + 1)
        while below:
            # Skip vert merged cells to get origin reference
            if not below.vert_merged:
                return below
            below = self.table.get_cell_on_grid(self.grid_x, below.grid_y + 1)
        return None

    @cached_property
    def cell_next(self) -> Cell | None:
        """Return next cell from table grid.

        Next cell always is an reference to common or restarting cell,
        so if you got cell `restart`, next cell after can be in another row.

        If you want next cell merged use `get_cell_on_grid` instead.

        Raises:
            TblPosError: If some refs is broken while positioning.

        Returns:
            Cell | None: Next cell or not.
        """
        # We want get ref on real (or merged) next cell not horizontally spanned
        grid_x_next = self.grid_x + self.horz_span
        next_ = self.table.get_cell_on_grid(grid_x_next, self.grid_y)
        if next_ is None:
            return None
        # Don't return merged cell, return restarting cell instead
        if next_.vert_merged:
            above = self.table.get_cell_on_grid(grid_x_next, self.grid_y - 1)
            while above:
                if not above.vert_merged:
                    return above
                above = self.table.get_cell_on_grid(
                    grid_x_next, above.grid_y - 1
                )
            msg = "Cannot get next cell: refs broken"
            raise TblPosError(msg)
        return next_

    @cached_property
    def cell_prev(self) -> Cell | None:
        """Return previous cell from table grid.

        Previous cell always is an reference to common or restarting cell,
        so if you got cell `restart`, previous cell after can be in another row.

        If you want previous cell merged use `get_cell_on_grid` instead.

        Raises:
            TblPosError: If some refs is broken while positioning.

        Returns:
            Cell | None: Previous cell or not.
        """
        # Saved ref in `cells_grid_x` of parent row will return merged or restart cell
        grid_x_prev = self.grid_x - 1
        prev = self.table.get_cell_on_grid(grid_x_prev, self.grid_y)
        if prev is None:
            return None
        # Don't return merged cell, return restarting cell instead
        if prev.vert_merged:
            above = self.table.get_cell_on_grid(grid_x_prev, self.grid_y - 1)
            while above:
                if not above.vert_merged:
                    return above
                above = self.table.get_cell_on_grid(
                    grid_x_prev, above.grid_y - 1
                )
            msg = "Cannot get previous cell: refs broken"
            raise TblPosError(msg)
        return prev

    @cached_property
    def is_first(self) -> bool:
        """Is first cell in current row grid."""
        return self.cell_prev is None

    @cached_property
    def is_last(self) -> bool:
        """Is last cell in current row grid."""
        return self.cell_next is None

    @cached_property
    def pos(self) -> POS:
        """Cell position on table grid relative to row."""
        return self.element.xml_position(self.is_first, self.is_last)

    @cached_property
    def vert_span(self) -> int | None:
        """Cells vertical span value like in HTML.

        Returns:
            int | None: Vertical span or None if it's
                vertically merged cell.
        """
        if self.vert_merged:
            return None
        if not self._vmerge == SE_MERGE.RESTART:
            return 1
        span = 1
        merged_below = self.table.get_cell_on_grid(
            self.grid_x, self.grid_y + span
        )
        while merged_below:
            if not merged_below.vert_merged:
                return span
            span += 1
            merged_below = self.table.get_cell_on_grid(
                self.grid_x, self.grid_y + span
            )
        return span

    @cached_property
    def _vmerge(self) -> NotFound | None | SE_MERGE:
        return self._prop("tcPr.vMerge.val", True)

    # TODO: here H2D

    @cached_property
    def table_style(self) -> TableStyle | None:
        return self.row.table_style

    @cached_property
    def _borders_non_zero_spacing_info(self) -> BordersInfo:
        inf = self._spacing_non_zero()
        inf["spacing"] = self._spacing
        return inf

    @cached_property
    def _spacing(self) -> Length | float | None:
        name = "tblCellSpacing"
        row = self.row
        tbl_h2d = row.table.h2d
        # Row-level direct
        spacing_elm = row._prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        # Row-level exception or Table-level direct
        spacing_elm = row._tblCellSpacing
        if spacing_elm is not None:
            return width(spacing_elm, True)

        # From table style (defined common or exception)
        path = self.path(f"trPr.{name}")
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
    def _cell_mar_ctx(
        self,
    ) -> tuple[CT_TcMar | None, TableStyle | CT_TblStylePr | None]:
        return self._prop_with_ctx("tcMar")

    @cached_property
    def _row_band_number(self) -> int:
        band_shift = 1 if self.row._shift_horz_bands else 0
        y_shift = self.grid_y + 1 + band_shift
        return y_shift // self.table.h2d._row_band_size

    @cached_property
    def _col_band_number(self) -> int:
        band_shift = 1 if self.row._shift_vert_bands else 0
        x_shift = self.idx + 1 + band_shift
        return x_shift // self.table.h2d._col_band_size

    @cached_property
    def _cnf_latent(self) -> WD_CNF_FORMAT:
        _CNF = WD_CNF_FORMAT
        cnf = _CNF(0)
        # Special rows/columns
        if self.grid_y == 0:
            cnf |= _CNF.FIRST_ROW
        if self.cell_below is None:
            cnf |= _CNF.LAST_ROW
        if self.grid_x == 0:
            cnf |= _CNF.FIRST_COLUMN
        if self.cell_next is None:
            cnf |= _CNF.LAST_COLUMN
        # Corner group
        if self.grid_y == 0 and self.grid_x == 0:
            cnf |= _CNF.FIRST_ROW_FIRST_COLUMN
        if self.grid_y == 0 and self.cell_next is None:
            cnf |= _CNF.FIRST_ROW_LAST_COLUMN
        if self.cell_below is None and self.grid_x == 0:
            cnf |= _CNF.LAST_ROW_FIRST_COLUMN
        if self.cell_below is None and self.cell_next is None:
            cnf |= _CNF.LAST_ROW_LAST_COLUMN
        # Horizontal/Vertical Bands
        has_vert_band_shift_group = (
            _CNF.FIRST_COLUMN & cnf
            or _CNF.FIRST_ROW_FIRST_COLUMN & cnf
            or _CNF.LAST_ROW_FIRST_COLUMN & cnf
            or _CNF.LAST_COLUMN & cnf
            or _CNF.FIRST_ROW_LAST_COLUMN & cnf
            or _CNF.LAST_ROW_LAST_COLUMN & cnf
        )
        if not (self.row._shift_vert_bands and has_vert_band_shift_group):
            if self._col_band_number % 2 == 0:
                cnf |= _CNF.EVEN_VERTICAL_BAND
            else:
                cnf |= _CNF.ODD_VERTICAL_BAND
        has_horz_band_shift_group = (
            _CNF.FIRST_ROW & cnf
            or _CNF.FIRST_ROW_FIRST_COLUMN & cnf
            or _CNF.FIRST_ROW_LAST_COLUMN & cnf
            or _CNF.LAST_ROW & cnf
            or _CNF.LAST_ROW_FIRST_COLUMN & cnf
            or _CNF.LAST_ROW_LAST_COLUMN & cnf
        )
        if not (self.row._shift_vert_bands and has_horz_band_shift_group):
            if self._row_band_number % 2 == 0:
                cnf |= _CNF.EVEN_HORIZONTAL_BAND
            else:
                cnf |= _CNF.ODD_HORIZONTAL_BAND
        return cnf

    @cached_property
    def _cnf_looked(self) -> WD_CNF_FORMAT:
        cnf = self._cnf_latent
        if not self.row.first_row_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
        if not self.row.last_row_show:
            cnf &= ~WD_CNF_FORMAT.LAST_ROW
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if not self.row.first_col_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
        if not self.row.last_col_show:
            cnf &= ~WD_CNF_FORMAT.LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if self.row.no_horizontal_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_HORIZONTAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND
        if self.row.no_vertical_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_VERTICAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_VERTICAL_BAND
        return cnf

    @cached_property
    def _tbl_style_props_deep(
        self,
    ) -> list[tuple[TableStyle, list[CT_TblStylePr]]]:
        tbl_style = self.table_style
        props_leveled = []
        cnf = self._cnf_looked
        while isinstance(tbl_style, TableStyle):
            tbl_style_props = self._table_style_props(tbl_style, cnf)
            props_leveled.append((tbl_style, tbl_style_props))
            tbl_style = self.document_part.styles.base_style(tbl_style)  # type: ignore[assignment]
        return props_leveled

    @cached_property
    def _self_top(self) -> Border | None:
        return self._self_border("top")

    @cached_property
    def _self_bottom(self) -> Border | None:
        return self._self_border("bottom")

    @cached_property
    def _self_left(self) -> Border | None:
        return self._self_border("left")

    @cached_property
    def _self_right(self) -> Border | None:
        return self._self_border("right")

    @cached_property
    def _border_grid_cells(self) -> list[CellOnBorderGrid]:
        cell_on_grids: list[CellOnBorderGrid] = []
        borders_ctx = self._tcBordersCtx
        if borders_ctx is None:
            return cell_on_grids
        for tcBorders_elm, ctx in borders_ctx:
            if ctx is None or isinstance(ctx, TableStyle):
                grid_group = SE_TBL_STYLE_OVERRIDE_TYPE.ENTIRE_TABLE
            else:
                grid_group = ctx.type
            cell_on_grids.append(
                CellOnBorderGrid(self, tcBorders_elm, grid_group)
            )
        return cell_on_grids

    @cached_property
    def _tcBordersCtx(
        self,
    ) -> list[tuple[CT_TcBorders, None | TableStyle | CT_TblStylePr]] | None:
        path = self.path("tcPr.tcBorders")
        tcBorders_elm = self._prop(path)
        if not isinstance(tcBorders_elm, NotFound):
            return [(tcBorders_elm, None)]
        ctx_list: list[
            tuple[CT_TcBorders, None | TableStyle | CT_TblStylePr]
        ] = []
        override_type_seen = set()
        for tbl_style, tbl_style_props in self._tbl_style_props_deep:
            if not tbl_style_props:
                tcBorders_elm = safe_get_prop(tbl_style.element, path, False)
                if not isinstance(tcBorders_elm, NotFound):
                    return [(tcBorders_elm, tbl_style)]
            for prop in tbl_style_props:
                tcBorders_elm = safe_get_prop(prop, path, False)
                if (
                    not isinstance(tcBorders_elm, NotFound)
                    and prop.type not in override_type_seen
                ):
                    ctx_list.append((tcBorders_elm, prop))
                    override_type_seen.add(prop.type)
        if ctx_list:
            return ctx_list
        return None

    def _self_border(self, border: _Border) -> Border | None:
        border_proxy = None
        for cell_grid in self._border_grid_cells:
            if border_proxy is None:
                border_proxy = getattr(cell_grid, border, None)
        return border_proxy

    def _spacing_zero(self, inf: BordersInfo) -> BordersInfo:
        self._vert_borders_conflict(inf)
        self._horz_borders_conflict(inf)
        return inf

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

    def _vert_borders_conflict(self, inf: BordersInfo) -> None:
        tbl_left = self.row._table_left
        tbl_right = self.row._table_right
        tbl_vert = self.row._table_insideV
        cell_prev = self.cell_prev
        cell_next = self.cell_next
        left_n, right_n = _TBL_POSITIONING[self.pos]["cell"]
        if left_n == "left":
            inf["left"] = Border.oppose(inf["left"], tbl_left)
        elif left_n == "insideV" and cell_prev is not None:
            prev_inf = cell_prev._borders_non_zero_spacing_info
            inf["left"] = Border.oppose(
                inf["left"], prev_inf["right"] or tbl_vert
            )
        if right_n == "right":
            inf["right"] = Border.oppose(inf["right"], tbl_right)
        elif right_n == "insideV" and cell_next is not None:
            next_inf = cell_next._borders_non_zero_spacing_info
            inf["right"] = Border.oppose(
                inf["right"], next_inf["left"] or tbl_vert
            )

    def _horz_borders_conflict(self, inf: BordersInfo) -> None:
        tbl_top = self.row._table_top
        tbl_bottom = self.row._table_bottom
        tbl_horz = self.row._table_insideH
        cell_above = self.cell_above
        cell_below = self.cell_below
        top_n, bottom_n = _TBL_POSITIONING[self.row.pos]["row"]

        if top_n == "top":
            inf["top"] = Border.oppose(inf["top"], tbl_top)
        elif top_n == "insideH" and cell_above is not None:
            above_inf = cell_above._borders_non_zero_spacing_info
            inf["top"] = Border.oppose(
                inf["top"], above_inf["bottom"] or tbl_horz
            )
        if bottom_n == "bottom":
            inf["bottom"] = Border.oppose(inf["bottom"], tbl_bottom)
        elif bottom_n == "insideH" and cell_below is not None:
            below_inf = cell_below._borders_non_zero_spacing_info
            inf["bottom"] = Border.oppose(
                inf["bottom"], below_inf["top"] or tbl_horz
            )

    def _choose_side(self, inf: BordersInfo, side_n: _Side) -> None:
        if side_n in ("top", "bottom"):
            table_inside = self.row._table_insideH
        else:
            table_inside = self.row._table_insideV
        side: Border | None = getattr(self, f"_self_{side_n}")
        if side is None and table_inside is not None:
            # Small hack to make the border comparator think that this side is more important
            table_inside._parent = self
            side = table_inside
        inf[side_n] = side

    def _prop_with_ctx(
        self, name: str
    ) -> tuple[Any | None, TableStyle | CT_TblStylePr | None]:
        elm = self._prop(name)
        if not isinstance(elm, NotFound):
            return elm, None
        path = self.path(f"tcPr.{name}")
        tc_ctx = self._from_tbl_style_hierarchy(
            self._tbl_style_props_deep, path
        )
        if not isinstance(tc_ctx[0], NotFound):
            return tc_ctx
        return None, None

    def _table_style_props(
        self, table_style: TableStyle, cnf: WD_CNF_FORMAT
    ) -> list[CT_TblStylePr]:
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
                tblStylePr_elm = table_style.bitwise_tbl_style_prop(flag)
                if tblStylePr_elm is not None:
                    props.append(tblStylePr_elm)
        if table_style.wholeTable:
            props.append(table_style.wholeTable)
        return props

    def _from_tbl_style_hierarchy(
        self,
        tbl_style_props_deep: list[tuple[TableStyle, list[CT_TblStylePr]]],
        path: PropertyPath,
        optional: bool = False,
    ) -> tuple[Any, TableStyle | CT_TblStylePr | None]:
        """Get property value from complex table style hierarchy.

        Here is 4 cases for 2nd value in tuple:
        1) For `None` there is no value from style hierarchy (can be found directly).
        2) For `CT_TblStylePr` you've got value from an grid group of and table style property.
        3) For `TableStyle` you've got an value from table style (can be an fallback or not).

        Args:
            tbl_style_props_deep (list[tuple[TableStyle, list[CT_TblStylePr]]]): Full list of an applied
                pairs `TableStyle` and table style properties inside from style hierarchy.
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            tuple[Any, TableStyle | CT_TblStylePr | None]: Context as pair of
                an got property value an applied table style or table style property (grid group)
                or `None`.
        """
        style_direct_val = NotFound(self, path)
        found_in_style = None
        for tbl_style, tbl_style_props in tbl_style_props_deep:
            if isinstance(style_direct_val, NotFound):
                style_direct_val = safe_get_prop(
                    tbl_style.element, path, optional
                )
                found_in_style = tbl_style
            tbl_val, tbl_style_prop = self._from_tbl_style_props(
                tbl_style_props, path, optional
            )
            if not isinstance(tbl_val, NotFound):
                return tbl_val, cast("CT_TblStylePr", tbl_style_prop)
        return style_direct_val, found_in_style

    def _from_tbl_style_props(
        self,
        table_style_props: list[CT_TblStylePr],
        path: PropertyPath,
        optional: bool = False,
    ) -> tuple[Any, CT_TblStylePr | None]:
        """Get property value from table style properties (grid group).

        Args:
            table_style_props (list[CT_TblStylePr]): Provided table style properties on an given table style level.
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            tuple[Any, CT_TblStylePr | None]: Tuple of found (`NotFound` instance or Any value) and in which
                table style property was found chosen property.
        """
        for tbl_style_prop in table_style_props:
            table_val = safe_get_prop(tbl_style_prop, path, optional)
            if isinstance(table_val, NotFound):
                continue
            return table_val, tbl_style_prop
        return NotFound(table_style_props, path), None

    def _prop_direct(self, path: str, optional: bool = False) -> Any:
        return self.prop(path, optional)

    def _prop_style(self, path: str, optional: bool = False) -> Any:
        if self.table_style:
            return from_style_inheritance(
                self, self.table_style, path, optional
            )
        return NotFound(self, path)

    def _prop(
        self,
        path: str,
        optional: bool = False,
        where: Literal["direct", "style", "both"] = "direct",
    ) -> Any:
        if where == "direct":
            return self._prop_direct(path, optional)
        elif where == "style":
            return self._prop_style(path, optional)
        direct_val = self._prop_direct(path, optional)
        if isinstance(direct_val, NotFound):
            return self._prop_style(path, optional)
        return direct_val

    # TODO: here H2D (end)
