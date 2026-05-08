from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.compute import width
from docxray.oxml.trans.proxy.shared import PropertyPath, Twips, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    TableStyle,
)
from docxray.oxml.trans.proxy.table import Cell, Row, Table
from docxray.oxml.trans.st.enums import SE_StyleType

from .resolver import Resolver


class TableResolver(Resolver[Table]):
    @cached_property
    def table_style(self) -> TableStyle:
        path = self._prop_path("val", "tblPr.tblStyle")
        style_id = safe_get_prop(self._proxy.element, path)
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class RowResolver(Resolver[Row]):
    @cached_property
    def table_resolver(self) -> TableResolver:
        return self._proxy.table.h2d._resolver

    @cached_property
    def table_style(self) -> TableStyle:
        return self.table_resolver.table_style

    @cached_property
    def cell_spacing(self) -> Twips | float | None:
        tblCellSpacing_elm = self._prop("tblCellSpacing")
        if tblCellSpacing_elm is None:
            return None
        return width(tblCellSpacing_elm)

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class CellResolver(Resolver[Cell]):
    @cached_property
    def row_resolver(self) -> RowResolver:
        return self._proxy.row.h2d._resolver

    @cached_property
    def table_resolver(self) -> TableResolver:
        return self.row_resolver.table_resolver

    @cached_property
    def table_style(self) -> TableStyle:
        return self.row_resolver.table_style

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
