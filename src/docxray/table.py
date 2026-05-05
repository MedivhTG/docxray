from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import cast

# docxray stuff
from docxray.blkcntnr import BlockItemContainer
from docxray.enum.word import WD_MERGE
from docxray.oxml.table.table import CT_Row, CT_Tbl, CT_Tc
from docxray.resolver.table import CellResolver, RowResolver, TableResolver
from docxray.shared import (
    ElementProxy,
    PropertyPath,
    StoryChild,
    safe_get_prop,
)


class Cell(BlockItemContainer[CT_Tc]):
    @cached_property
    def resolver(self) -> CellResolver:
        return CellResolver(self.element, self.part.document_part, "")

    @cached_property
    def row(self) -> Row:
        return cast("Row", self._parent)

    @cached_property
    def idx(self) -> int:
        return self.row.cells_alive.index(self)

    @cached_property
    def next_cell_alive(self) -> Cell | None:
        return self.row.get_cell_alive(self.idx + 1)

    @cached_property
    def prev_cell_alive(self) -> Cell | None:
        return self.row.get_cell_alive(self.idx - 1)


class Row(ElementProxy[CT_Row]):
    @cached_property
    def resolver(self) -> RowResolver:
        return RowResolver(self.element, self.part, "NO")  # type: ignore[arg-type]

    @cached_property
    def cells_alive(self) -> list[Cell]:
        cells = []
        for tc_elm in self.element.tc_lst:
            vMerge_val = safe_get_prop(
                tc_elm, PropertyPath.base("val", "tcPr.vMerge")
            )
            if vMerge_val == WD_MERGE.CONTINUE:
                continue
            cells.append(Cell(tc_elm, self))  # type: ignore[arg-type]
        return cells

    def iter_cells(self) -> Iterator[Cell]:
        for cell in self.cells_alive:
            yield cell

    def get_cell_alive(self, idx: int) -> Cell | None:
        if idx < 0:
            return None
        if idx > len(self.cells_alive) - 1:
            return None
        return self.cells_alive[idx]


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def resolver(self) -> TableResolver:
        return TableResolver(self.element, self.part.document_part, "NO")

    def iter_rows(self) -> Iterator[Row]:
        for tr_elm in self.element.tr_lst:
            yield Row(tr_elm, self)
