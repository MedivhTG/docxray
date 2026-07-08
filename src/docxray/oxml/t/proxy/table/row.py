from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.length import Length, Twips
from docxray.oxml.t.proxy.compute import twips_measure
from docxray.oxml.t.proxy.base import ElementProxy, NotFound
from docxray.oxml.t.st.enums import SE_HEIGHT_RULE
from docxray.oxml.t.table.row_props import CT_Height
from docxray.oxml.t.table.table import CT_Row

from .cell import Cell

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.h2d.row_h2d import RowH2D

    from .table import Table


class Row(ElementProxy[CT_Row]):
    @cached_property
    def h2d(self) -> RowH2D:
        # docxray stuff
        from docxray.oxml.t.h2d.row_h2d import RowH2D

        return RowH2D(self, self.part, "trPr")  # type: ignore[arg-type]

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
        trHeight_elm: CT_Height | NotFound = self.h2d._prop("trHeight")
        if isinstance(trHeight_elm, NotFound):
            return SE_HEIGHT_RULE.AUTO
        rule = trHeight_elm.hRule
        if rule is None:
            return SE_HEIGHT_RULE.AUTO
        return rule

    @cached_property
    def height(self) -> Length | None:
        """Row height in twips or percents, `None` if auto."""
        trHeight_elm: CT_Height | NotFound = self.h2d._prop("trHeight")
        if isinstance(trHeight_elm, NotFound):
            return None
        val = trHeight_elm.val
        if val is None:
            return Twips(0)
        return twips_measure(val)

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
