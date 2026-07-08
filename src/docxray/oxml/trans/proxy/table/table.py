from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.length import Length
from docxray.oxml.trans.proxy.base import StoryChild
from docxray.oxml.trans.st.enums import SE_JC_TABLE, SE_TBL_LAYOUT_TYPE
from docxray.oxml.trans.table.table import CT_Tbl

from .cell import Cell
from .row import Row

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.table_h2d import TableH2D
    from docxray.oxml.trans.proxy.document import Body
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def h2d(self) -> TableH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.table_h2d import TableH2D

        return TableH2D(self, self.part, "tblPr")  # type: ignore[arg-type]

    @cached_property
    def container(self) -> Body | Cell:
        return cast("Body | Cell", self._parent)

    @cached_property
    def content_idx(self) -> int:
        return self.container.inner_content.index(self)

    @cached_property
    def prev_content_item(self) -> Paragraph | Table | None:
        prev_idx = self.content_idx - 1
        if prev_idx < 0:
            return None
        return self.container.inner_content[prev_idx]

    @cached_property
    def next_content_item(self) -> Paragraph | Table | None:
        next_idx = self.content_idx + 1
        if next_idx + 1 > len(self.container.inner_content):
            return None
        return self.container.inner_content[next_idx]

    @cached_property
    def left_indent(self) -> Length | float | None:
        return self.h2d.left_indent

    @cached_property
    def alignment(self) -> SE_JC_TABLE:
        return self.h2d.alignment

    @cached_property
    def width(self) -> Length | float | None:
        return self.h2d.width

    @cached_property
    def layout(self) -> SE_TBL_LAYOUT_TYPE:
        return self.h2d.table_layout

    @cached_property
    def rows(self) -> list[Row]:
        return [Row(tr_elm, self) for tr_elm in self.element.tr_lst]

    @cached_property
    def spacing_first(self) -> Length | float | None:
        """Get firsct spacing value in the table inside of cells.

        This property is for determining spacing between cells in the table.
        But not use it if you want accurate reprsentation of Word cells, cause
        each cell has own cell spacing actually.

        Returns:
            Length | float | None: If `Length` - EMU value, elif `float` - percents,
                else no spacing.
        """
        for row in self.iter_rows():
            for cell in row.iter_cells():
                spacing = cell.borders_info["spacing"]
                if spacing is not None:
                    return spacing
        return None

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
