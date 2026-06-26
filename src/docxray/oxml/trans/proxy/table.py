from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.enum.lxml import POS
from docxray.oxml.trans.proxy.blkcntnr import BlockItemContainer
from docxray.oxml.trans.st.enums import (
    SE_HEIGHT_RULE,
    SE_JC_TABLE,
    SE_TBL_LAYOUT_TYPE,
    SE_TEXT_DIRECTION,
    SE_VERTICAL_JC,
    SE_Merge,
)
from docxray.oxml.trans.table.row_props import CT_Height
from docxray.oxml.trans.table.table import CT_Row, CT_Tbl, CT_Tc
from docxray.transform.transformer import Transformer

from .compute import twips_measure, width
from .shared import ElementProxy, Length, NotFound, StoryChild, Twips

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.cell_h2d import (
        BordersInfo,
        CellH2D,
        PaddingInfo,
    )
    from docxray.oxml.trans.h2d.row_h2d import RowH2D
    from docxray.oxml.trans.h2d.table_h2d import TableH2D
    from docxray.oxml.trans.proxy.document import Body
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph
    from docxray.transform.ruleset import RuleSet
    from docxray.transform.transformer import TransformMethod


class TblPosError(Exception):
    pass


class Cell(BlockItemContainer[CT_Tc]):
    @cached_property
    def h2d(self) -> CellH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.cell_h2d import CellH2D

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
    def width(self) -> Twips | float | None:
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
        if self._vmerge in (None, SE_Merge.CONTINUE):
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
        return self.h2d._prop_val("vMerge", optional=True)


class Row(ElementProxy[CT_Row]):
    @cached_property
    def h2d(self) -> RowH2D:
        from ..h2d.row_h2d import RowH2D

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


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def h2d(self) -> TableH2D:
        from ..h2d.table_h2d import TableH2D

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

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(self, ruleset, "Table", stringify, method)
