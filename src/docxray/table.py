from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import cast

# docxray stuff
from docxray.blkcntnr import BlockItemContainer
from docxray.enum.lxml import XML_POSITION
from docxray.enum.word import WD_MERGE
from docxray.oxml.table.table import CT_Row, CT_Tbl, CT_Tc
from docxray.resolver.table import CellResolver, RowResolver, TableResolver
from docxray.shared import (
    ElementProxy,
    PropertyPath,
    StoryChild,
    position,
    safe_get_prop,
)


class Cell(BlockItemContainer[CT_Tc]):
    @cached_property
    def resolver(self) -> CellResolver:
        return CellResolver(self.element, self.part.document_part, "tcPr")

    @cached_property
    def row(self) -> Row:
        return cast("Row", self._parent)

    @cached_property
    def table(self) -> Table:
        return self.row.table

    @cached_property
    def idx(self) -> int:
        return self.row.cells.index(self)

    @cached_property
    def grid_x(self) -> int:
        path = PropertyPath.base("horz_span")
        return sum(
            safe_get_prop(self.row.get_cell(i), path, 1)
            for i in range(self.idx)
        )

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
        return self.table.cell_on_grid(self.grid_x, self.grid_y + 1)

    @cached_property
    def cell_above(self) -> Cell | None:
        return self.table.cell_on_grid(self.grid_x, self.grid_y - 1)

    @cached_property
    def vmerge(self) -> WD_MERGE | None:
        path = PropertyPath.base("val", "tcPr.vMerge")
        return safe_get_prop(self.element, path)

    @cached_property
    def vert_merged(self) -> bool:
        if self.vmerge == WD_MERGE.CONTINUE:
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
    def pos(self) -> XML_POSITION:
        return position(self.is_first, self.is_last)

    @cached_property
    def horz_span(self) -> int:
        path = PropertyPath.base("val", "tcPr.gridSpan")
        return safe_get_prop(self.element, path, 1)

    @cached_property
    def vert_span(self) -> int:
        if self.vmerge is None:
            return 1
        if self.vmerge == WD_MERGE.CONTINUE:
            return -1
        below = self.cell_below
        span = 1
        while below:
            if not below.vert_merged:
                return span
            span += 1
            below = below.cell_below
        return span


class Row(ElementProxy[CT_Row]):
    @cached_property
    def resolver(self) -> RowResolver:
        return RowResolver(self.element, self.part, "trPr")  # type: ignore[arg-type]

    @cached_property
    def table(self) -> Table:
        return cast("Table", self._parent)

    @cached_property
    def idx(self) -> int:
        return self.table.rows.index(self)

    @cached_property
    def cells(self) -> list[Cell]:
        return [Cell(tc_elm, self) for tc_elm in self.element.tc_lst]  # type: ignore[arg-type]

    def iter_cells(self) -> Iterator[Cell]:
        for cell in self.cells:
            yield cell

    def get_cell(self, idx: int) -> Cell | None:
        if idx < 0:
            return None
        if idx > len(self.cells) - 1:
            return None
        return self.cells[idx]


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def resolver(self) -> TableResolver:
        return TableResolver(self.element, self.part.document_part, "tblPr")

    @cached_property
    def rows(self) -> list[Row]:
        return [Row(tr_elm, self) for tr_elm in self.element.tr_lst]

    def get_row(self, idx: int) -> Row | None:
        if idx < 0:
            return None
        if idx > len(self.rows) - 1:
            return None
        return self.rows[idx]

    def cell_on_grid(self, x: int, y: int) -> Cell | None:
        row = self.get_row(y)
        if row is None:
            return None
        cell = row.get_cell(x)
        if cell is None:
            return None
        return cell

    def iter_rows(self) -> Iterator[Row]:
        for row in self.rows:
            yield row
