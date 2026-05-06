from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.compute import width
from docxray.oxml.trans.proxy.shared import PropertyPath, Twips
from docxray.oxml.trans.proxy.table import Cell, Row, Table
from docxray.oxml.trans.st.enums import SE_Border

from .resolver import BaseResolver


class TableResolver(BaseResolver[Table]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class RowResolver(BaseResolver[Row]):
    @cached_property
    def cell_spacing(self) -> Twips | float | None:
        tblCellSpacing_elm = self._prop("tblCellSpacing")
        if tblCellSpacing_elm is None:
            return None
        return width(tblCellSpacing_elm)

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return self._from_table_style(self._story.table.element, property_path)


class CellResolver(BaseResolver[Cell]):
    @cached_property
    def row_resolver(self) -> RowResolver:
        return RowResolver(self._story.row, self._document_part, "trPr")

    @cached_property
    def width(self) -> Twips | float | None:
        tcW_elm = self._prop("tcW", only_direct=True)
        if tcW_elm is None:
            return None
        return width(tcW_elm)

    @cached_property
    def top(self) -> SE_Border | None:
        return self._prop_val("top")

    @cached_property
    def bottom(self) -> SE_Border | None:
        return self._prop_val("bottom")

    @cached_property
    def left(self) -> SE_Border | None:
        return self._prop_val("left")

    @cached_property
    def right(self) -> SE_Border | None:
        return self._prop_val("right")

    @cached_property
    def inside_horizontal(self) -> SE_Border | None:
        return self._prop_val("insideH")

    @cached_property
    def inside_vertical(self) -> SE_Border | None:
        return self._prop_val("insideV")

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
