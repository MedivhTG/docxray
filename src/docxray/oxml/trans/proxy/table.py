from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.oxml.trans.proxy.blkcntnr import BlockItemContainer
from docxray.oxml.trans.st.enums import SE_Merge
from docxray.oxml.trans.table.table import CT_Row, CT_Tbl, CT_Tc

from .compute import width
from .shared import ElementProxy, NotFound, StoryChild, Twips

if TYPE_CHECKING:
    from .h2d.table_h2d import CellH2D, RowH2D, TableH2D


class TblPosError(Exception):
    pass


class Cell(BlockItemContainer[CT_Tc]):
    @cached_property
    def h2d(self) -> CellH2D:
        from .h2d.table_h2d import CellH2D
        from .h2d.table_rslv import CellResolver

        return CellH2D(CellResolver(self, self.part.document_part, "tcPr"))

    @cached_property
    def row(self) -> Row:
        return cast("Row", self._parent)

    @cached_property
    def table(self) -> Table:
        return self.row.table

    @cached_property
    def width(self) -> Twips | float | None:
        tcW_elm = self.h2d._rslvr.prop("tcW")
        if isinstance(tcW_elm, NotFound) or tcW_elm is None:
            return None
        return width(tcW_elm)

    @cached_property
    def horz_span(self) -> int:
        gridSpan_val = self.h2d._rslvr.prop_val("gridSpan")
        if isinstance(gridSpan_val, NotFound):
            return 1
        return gridSpan_val

    @cached_property
    def idx(self) -> int:
        return self.row.cells.index(self)

    @cached_property
    def grid_x(self) -> int:
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
        return self.row.idx

    @cached_property
    def vert_merged(self) -> bool:
        if self._vmerge in (None, SE_Merge.CONTINUE):
            return True
        return False

    @cached_property
    def cell_above(self) -> Cell | None:
        above = self.table.get_cell_on_grid(self.grid_x, self.grid_y - 1)
        while above:
            # Skip vert merged cells to get origin reference
            if not above.vert_merged:
                return above
            above = self.table.get_cell_on_grid(self.grid_x, above.grid_y - 1)
        return None

    @cached_property
    def cell_below(self) -> Cell | None:
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
        return self.cell_prev is None

    @cached_property
    def is_last(self) -> bool:
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
        if not self._vmerge == SE_Merge.RESTART:
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
    def _vmerge(self) -> NotFound | None | SE_Merge:
        return self.h2d._rslvr.prop_val("vMerge", optional=True)


class Row(ElementProxy[CT_Row]):
    @cached_property
    def h2d(self) -> RowH2D:
        from .h2d.table_h2d import RowH2D
        from .h2d.table_rslv import RowResolver

        return RowH2D(RowResolver(self, self.part, "trPr"))  # type: ignore[arg-type]

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
        try:
            return self.cells_grid_x[grid_x]
        except KeyError:
            return None


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def h2d(self) -> TableH2D:
        from .h2d.table_h2d import TableH2D
        from .h2d.table_rslv import TableResolver

        return TableH2D(TableResolver(self, self.part, "tblPr"))  # type: ignore[arg-type]

    @cached_property
    def rows(self) -> list[Row]:
        return [Row(tr_elm, self) for tr_elm in self.element.tr_lst]

    def get_row(self, idx: int) -> Row | None:
        if idx < 0:
            return None
        if idx > len(self.rows) - 1:
            return None
        return self.rows[idx]

    def get_cell_on_grid(self, grid_x: int, grid_y: int) -> Cell | None:
        """Get cell on grid by Ox (columns) and Oy (rows).

        Returned cell can be vertically merged (prop `vert_merged`),
        so don't use it on your calculations. Or cell can be a reference
        to horizontally spanned cell (you will see real xy pos).
        Else it will be an common cell.

        Args:
            grid_x (int): Ox pos of the cell in table grid.
            grid_y (int): Oy pos of the cell in table grid.

        Returns:
            Cell | None: Cell on table grid or None if not found.
        """
        row = self.get_row(grid_y)
        if row is None:
            return None
        return row.get_cell_on_grid(grid_x)

    def iter_rows(self) -> Iterator[Row]:
        for row in self.rows:
            yield row
