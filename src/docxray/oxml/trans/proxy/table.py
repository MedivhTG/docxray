from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.enum.lxml import XML_POSITION
from docxray.oxml.trans.proxy.blkcntnr import BlockItemContainer
from docxray.oxml.trans.st.enums import SE_Merge
from docxray.oxml.trans.table.table import CT_Row, CT_Tbl, CT_Tc

from .compute import width
from .shared import ElementProxy, NotFound, StoryChild, Twips

if TYPE_CHECKING:
    from .h2d.table_h2d import CellH2D, RowH2D, TableH2D


class Cell(BlockItemContainer[CT_Tc]):
    """Cell as `<w:tc>` in table.

    Some properties used directly (not from resolver) such as
    `gridSpan`, `vMerge`, `hMerge` (deprecated) and `tcW` by the reason:
    those properties affects the table grid and cannot be resolved
    from styles (it will break document).
    """

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
        """Width as `<w:tcW>` attr of `w:w`.

        Returns:
            Twips | int | None: If `None` - than
                it's auto width; elif `float` than it's
                percentage of table width; else standard
                Word measure in `Twips`.
        """
        tcW_elm = self.h2d._rslvr.prop("tcW")
        if isinstance(tcW_elm, NotFound) or tcW_elm is None:
            return None
        return width(tcW_elm)

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
    def next_cell(self) -> Cell | None:
        return self.row.get_cell(self.idx + 1)

    @cached_property
    def prev_cell(self) -> Cell | None:
        return self.row.get_cell(self.idx - 1)

    @cached_property
    def cell_below(self) -> Cell | None:
        return self.table.get_cell_on_grid(self.grid_x, self.grid_y + 1)

    @cached_property
    def cell_above(self) -> Cell | None:
        return self.table.get_cell_on_grid(self.grid_x, self.grid_y - 1)

    @cached_property
    def vert_merged(self) -> bool:
        if self._vmerge in (None, SE_Merge.CONTINUE):
            return True
        return False

    @cached_property
    def is_first(self) -> bool:
        prev_cell = self.prev_cell
        while prev_cell:
            if not prev_cell.vert_merged:
                return False
            prev_cell = prev_cell.prev_cell
        return True

    @cached_property
    def is_last(self) -> bool:
        next_cell = self.next_cell
        while next_cell:
            if not next_cell.vert_merged:
                return False
            next_cell = next_cell.next_cell
        return True

    @cached_property
    def xml_pos(self) -> XML_POSITION:
        return self.element.xml_position(self.is_first, self.is_last)

    @cached_property
    def horz_span(self) -> int:
        gridSpan_val = self.h2d._rslvr.prop_val("gridSpan")
        if isinstance(gridSpan_val, NotFound):
            return 1
        return gridSpan_val

    @cached_property
    def vert_span(self) -> int:
        if self._vmerge is None:
            return 1
        if self._vmerge == SE_Merge.CONTINUE:
            return -1
        below = self.cell_below
        span = 1
        while below:
            if not below.vert_merged:
                return span
            span += 1
            below = below.cell_below
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
    def cells_grid(self) -> dict[int, Cell]:
        return {cell.grid_x: cell for cell in self.cells}

    @cached_property
    def xml_pos(self) -> XML_POSITION:
        return self.element.xml_pos

    def iter_cells(self) -> Iterator[Cell]:
        for cell in self.cells:
            yield cell

    def get_cell(self, idx: int) -> Cell | None:
        if idx < 0:
            return None
        if idx > len(self.cells) - 1:
            return None
        return self.cells[idx]

    def get_cell_on_grid(self, grid_x: int) -> Cell | None:
        try:
            return self.cells_grid[grid_x]
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
        row = self.get_row(grid_y)
        if row is None:
            return None
        return row.get_cell_on_grid(grid_x)

    def iter_rows(self) -> Iterator[Row]:
        for row in self.rows:
            yield row
