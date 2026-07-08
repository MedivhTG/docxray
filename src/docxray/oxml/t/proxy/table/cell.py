from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.length import Length
from docxray.oxml.t.proxy.blkcntnr import BlockItemContainer
from docxray.oxml.t.proxy.compute import width
from docxray.oxml.t.proxy.base import NotFound
from docxray.oxml.t.st.enums import (
    SE_TEXT_DIRECTION,
    SE_VERTICAL_JC,
    SE_MERGE,
)
from docxray.oxml.t.table.table import CT_Tc

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.h2d.cell_h2d import (
        BordersInfo,
        CellH2D,
        PaddingInfo,
    )

    from .row import Row
    from .table import Table


class TblPosError(Exception):
    pass


class Cell(BlockItemContainer[CT_Tc]):
    @cached_property
    def h2d(self) -> CellH2D:
        # docxray stuff
        from docxray.oxml.t.h2d.cell_h2d import CellH2D

        return CellH2D(self, self.part.document_part, "tcPr")

    @cached_property
    def borders_info(self) -> BordersInfo:
        """Primitive info about borders for current cell. Can be changed in future."""
        return self.h2d.borders_info

    @cached_property
    def padding_info(self) -> PaddingInfo:
        return self.h2d.padding_info

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
        return self.h2d.vertical_align

    @cached_property
    def content_flow(self) -> SE_TEXT_DIRECTION | None:
        return self.h2d.content_flow

    @cached_property
    def width(self) -> Length | float | None:
        """Cell width in twips or percents, `None` if auto."""
        tcW_elm = self.h2d._prop("tcW")
        if isinstance(tcW_elm, NotFound) or tcW_elm is None:
            return None
        return width(tcW_elm)

    @cached_property
    def horz_span(self) -> int:
        """Horizontal span of cells number like in HTML."""
        gridSpan_val = self.h2d._prop_val("gridSpan")
        if isinstance(gridSpan_val, NotFound):
            return 1
        return gridSpan_val

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
        return self.h2d._prop_val("vMerge", optional=True)
