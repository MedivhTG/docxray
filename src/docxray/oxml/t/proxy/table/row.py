from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.length import Length, Twips
from docxray.oxml.t.enums import WD_CNF_FORMAT, WD_CNF_TABLE_LOOK, CnfLookName
from docxray.oxml.t.proxy.base import (
    ElementProxy,
    NotFound,
    from_style_inheritance,
    safe_get_prop,
)
from docxray.oxml.t.proxy.border import Border
from docxray.oxml.t.proxy.compute import twips_measure
from docxray.oxml.t.proxy.styles.style import TableStyle
from docxray.oxml.t.shared import CT_Shd, CT_TblWidth
from docxray.oxml.t.st.enums import SE_HEIGHT_RULE, SE_TBL_STYLE_OVERRIDE_TYPE
from docxray.oxml.t.styles import CT_TblStylePr
from docxray.oxml.t.table.row_props import CT_Height
from docxray.oxml.t.table.table import CT_Row
from docxray.oxml.t.table.table_props import (
    CT_JcTable,
    CT_TblBorders,
    CT_TblCellMar,
    CT_TblLayoutType,
)

from .cell import Cell

if TYPE_CHECKING:
    from .table import Table

type _TblBorder = Literal[
    "top", "bottom", "left", "right", "insideH", "insideV"
]
_SHIFT_HORZ_BANDS = {
    SE_TBL_STYLE_OVERRIDE_TYPE.HEADER_ROW,
    SE_TBL_STYLE_OVERRIDE_TYPE.TOP_LEFT_CORNER_CELL,
    SE_TBL_STYLE_OVERRIDE_TYPE.TOP_RIGHT_CORNER_CELL,
}
_SHIFT_VERT_BANDS = {
    SE_TBL_STYLE_OVERRIDE_TYPE.FIRST_COLUMN,
    SE_TBL_STYLE_OVERRIDE_TYPE.TOP_LEFT_CORNER_CELL,
    SE_TBL_STYLE_OVERRIDE_TYPE.BOTTOM_LEFT_CORNER_CELL,
}


class Row(ElementProxy[CT_Row]):
    @cached_property
    def table(self) -> Table:
        return cast("Table", self._parent)

    @cached_property
    def idx(self) -> int:
        return self.table.rows.index(self)

    @cached_property
    def cells(self) -> list[Cell]:
        return [Cell(tc_elm, self) for tc_elm in self.element.tc_lst]  # type: ignore[arg-type]

    @cached_property
    def cells_grid_x(self) -> dict[int, Cell]:
        grid = {}
        for cell in self.cells:
            # Save reference for right positioning adjacent cells
            if cell.horz_span > 1:
                for x in range(cell.grid_x, cell.grid_x + cell.horz_span):
                    grid[x] = cell
            else:
                grid[cell.grid_x] = cell
        return grid

    @cached_property
    def pos(self) -> POS:
        return self.element.xml_pos

    @cached_property
    def height_rule(self) -> SE_HEIGHT_RULE:
        trHeight_elm: CT_Height | NotFound = self._prop("trPr.trHeight")
        if isinstance(trHeight_elm, NotFound):
            return SE_HEIGHT_RULE.AUTO
        rule = trHeight_elm.hRule
        if rule is None:
            return SE_HEIGHT_RULE.AUTO
        return rule

    @cached_property
    def height(self) -> Length | None:
        """Row height in twips or percents, `None` if auto."""
        trHeight_elm: CT_Height | NotFound = self._prop("trPr.trHeight")
        if isinstance(trHeight_elm, NotFound):
            return None
        val = trHeight_elm.val
        if val is None:
            return Twips(0)
        return twips_measure(val)

    @cached_property
    def first_row_show(self) -> bool:
        return self._format_from_cnf_look("firstRow")

    @cached_property
    def last_row_show(self) -> bool:
        return self._format_from_cnf_look("lastRow")

    @cached_property
    def first_col_show(self) -> bool:
        return self._format_from_cnf_look("firstColumn")

    @cached_property
    def last_col_show(self) -> bool:
        return self._format_from_cnf_look("lastColumn")

    @cached_property
    def no_horizontal_lines(self) -> bool:
        return self._format_from_cnf_look("noHBand")

    @cached_property
    def no_vertical_lines(self) -> bool:
        return self._format_from_cnf_look("noVBand")

    @cached_property
    def table_style(self) -> TableStyle | None:
        return self.table.table_style

    @cached_property
    def _latent_tbl_style_props(self) -> list[CT_TblStylePr]:
        if self.table_style is None:
            return []
        return self.table_style.table_style_props(WD_CNF_FORMAT(0xFFF))

    @cached_property
    def _shift_horz_bands(self) -> bool:
        for prop in self._latent_tbl_style_props:
            if prop.type in _SHIFT_HORZ_BANDS:
                return True
        return False

    @cached_property
    def _shift_vert_bands(self) -> bool:
        for prop in self._latent_tbl_style_props:
            if prop.type in _SHIFT_VERT_BANDS:
                return True
        return False

    @cached_property
    def _table_top(self) -> Border | None:
        return self._table_border("top")

    @cached_property
    def _table_bottom(self) -> Border | None:
        return self._table_border("bottom")

    @cached_property
    def _table_left(self) -> Border | None:
        return self._table_border("left")

    @cached_property
    def _table_right(self) -> Border | None:
        return self._table_border("right")

    @cached_property
    def _table_insideH(self) -> Border | None:
        return self._table_border("insideH")

    @cached_property
    def _table_insideV(self) -> Border | None:
        return self._table_border("insideV")

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        mask = self._prop("tblPrEx.tblLook.val")
        if not isinstance(mask, NotFound):
            WD_CNF_TABLE_LOOK.from_bytes(mask)
        return self.table._cnf_look

    @cached_property
    def _tblW(self) -> CT_TblWidth | None:
        return self._ex_or_table_prop("tblW")

    @cached_property
    def _jc(self) -> CT_JcTable | None:
        return self._ex_or_table_prop("jc")

    @cached_property
    def _tblCellSpacing(self) -> CT_TblWidth | None:
        prop = self._prop("trPr.tblCellSpacing")
        if isinstance(prop, NotFound):
            return self._ex_or_table_prop("tblCellSpacing")
        return prop

    @cached_property
    def _tblInd(self) -> CT_TblWidth | None:
        return self._ex_or_table_prop("tblInd")

    @cached_property
    def _tblBorders(self) -> CT_TblBorders | None:
        return self._ex_or_table_prop("tblBorders")

    @cached_property
    def _shd(self) -> CT_Shd | None:
        return self._ex_or_table_prop("shd")

    @cached_property
    def _tblLayout(self) -> CT_TblLayoutType | None:
        return self._ex_or_table_prop("tblLayout")

    @cached_property
    def _tblCellMar(self) -> CT_TblCellMar | None:
        return self._ex_or_table_prop("tblCellMar")

    def iter_cells(self, skip_merged: bool = True) -> Iterator[Cell]:
        """Iterate over xml-cell proxies in a row.

        Args:
            skip_merged (bool, optional): Skip vertically merged
                cells. Defaults to True.

        Yields:
            Iterator[Cell]: Next cell in a row.
        """
        for cell in self.cells:
            if skip_merged and cell.vert_merged:
                continue
            yield cell

    def get_cell(self, idx: int) -> Cell | None:
        if idx < 0:
            return None
        if idx > len(self.cells) - 1:
            return None
        return self.cells[idx]

    def get_cell_on_grid(self, grid_x: int) -> Cell | None:
        """Get cell on grid by Ox (columns).

        Returned cell can be vertically merged (prop `vert_merged`),
        so don't use it on your calculations. Or cell can be a reference
        to  horizontally spanned cell (you will see real xy pos).
        Else it will be an common cell.

        Args:
            grid_x (int): Ox pos of the cell in table grid.

        Returns:
            Cell | None: Cell on table grid or None if not found.
        """
        return self.cells_grid_x.get(grid_x)

    def _table_border(self, side: _TblBorder) -> Border | None:
        side_elm = safe_get_prop(self._tblBorders, self.path(side), False)
        if not isinstance(side_elm, NotFound):
            return Border(side_elm, self)
        return None

    def _format_from_cnf_look(self, format_name: CnfLookName) -> bool:
        return self._cnf_look.has_format(format_name)

    def _ex_or_table_prop(self, name: str) -> Any | None:
        prop = self.prop(f"tblPrEx.{name}")
        if isinstance(prop, NotFound):
            return self.table._table_prop(name)
        return prop

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
