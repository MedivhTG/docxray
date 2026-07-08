from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, cast

# docxray stuff
from docxray.length import Length
from docxray.oxml.t.enums import WD_CNF_TABLE_LOOK
from docxray.oxml.t.proxy.base import (
    NotFound,
    StoryChild,
    from_style_inheritance,
)
from docxray.oxml.t.proxy.compute import width
from docxray.oxml.t.proxy.styles.style import TableStyle
from docxray.oxml.t.st.enums import (
    SE_JC_TABLE,
    SE_STYLE_TYPE,
    SE_TBL_LAYOUT_TYPE,
)
from docxray.oxml.t.table.table import CT_Tbl

from .cell import Cell
from .row import Row

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.document import Body
    from docxray.oxml.t.proxy.text.paragraph import Paragraph


class Table(StoryChild[CT_Tbl]):
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
        tblInd_elm = self._prop("tblPr.tblInd", where="both")
        if isinstance(tblInd_elm, NotFound):
            return None
        return width(tblInd_elm)

    @cached_property
    def alignment(self) -> SE_JC_TABLE:
        align = self._prop("tblPr.jc", where="both")
        if isinstance(align, NotFound):
            return SE_JC_TABLE.LEFT
        return align

    @cached_property
    def width(self) -> Length | float | None:
        tblW_elm = self._prop("tblPr.tblW")
        if isinstance(tblW_elm, NotFound):
            return None
        return width(tblW_elm)

    @cached_property
    def layout(self) -> SE_TBL_LAYOUT_TYPE:
        layout = self._prop("tblPr.tblLayout.type")
        if isinstance(layout, NotFound):
            return SE_TBL_LAYOUT_TYPE.AUTOFIT
        return layout

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

    # TODO: here H2D

    @cached_property
    def table_style(self) -> TableStyle | None:
        style_id = self._prop("tblPr.tblStyle.val")
        if isinstance(style_id, NotFound):
            return None
        return self.document_part.styles.get_by_id(
            style_id, SE_STYLE_TYPE.TABLE, TableStyle
        )

    @cached_property
    def _row_band_size(self) -> int:
        size = self._prop("tblPr.tblStyleRowBandSize.val", where="style")
        if isinstance(size, NotFound):
            return 1
        return size

    @cached_property
    def _col_band_size(self) -> int:
        size = self._prop("tblPr.tblStyleColBandSize.val", where="style")
        if isinstance(size, NotFound):
            return 1
        return size

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        mask: bytes | None = self._prop("tblPr.tblLook.val", True)
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)

    def _table_prop(self, name: str) -> Any:
        elm = self._prop(f"tblPr.{name}", where="both")
        if isinstance(elm, NotFound):
            return None
        return elm

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
