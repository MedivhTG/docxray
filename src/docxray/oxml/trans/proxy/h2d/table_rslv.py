from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    TableStyle,
)
from docxray.oxml.trans.proxy.table import Cell, Row, Table
from docxray.oxml.trans.st.enums import SE_StyleType
from docxray.oxml.trans.table.table_props import CT_TblPrEx

from .resolver import Resolver


class TableResolver(Resolver[Table]):
    @cached_property
    def table_style(self) -> TableStyle | None:
        style_id = self.prop_val("tblStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    def from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> NotFound | None:
        if self.table_style is None:
            return NotFound(self, path)
        return self.from_style_inheritance(self.table_style, path, optional)


class RowResolver(Resolver[Row]):
    @cached_property
    def table(self) -> Table:
        return self._proxy.table

    @cached_property
    def table_resolver(self) -> TableResolver:
        return self.table.h2d._rslvr

    @cached_property
    def tblPrEx(self) -> CT_TblPrEx | None:
        tblPrEx_elm = self.prop("tblPrEx")
        if isinstance(tblPrEx_elm, NotFound):
            return None
        return tblPrEx_elm

    @cached_property
    def table_style(self) -> TableStyle | None:
        if self.tblPrEx is None:
            return self.table_resolver.table_style
        style_id = safe_get_prop(
            self.tblPrEx, self.prop_path("val", "tblStyle"), False
        )
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    def from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self.table_style is None:
            return NotFound(self, path)
        return self.from_style_inheritance(self.table_style, path, optional)


class CellResolver(Resolver[Cell]):
    @cached_property
    def row(self) -> Row:
        return self._proxy.row

    @cached_property
    def row_resolver(self) -> RowResolver:
        return self.row.h2d._rslvr

    @cached_property
    def table_resolver(self) -> TableResolver:
        return self.row_resolver.table_resolver

    @cached_property
    def table_style(self) -> TableStyle | None:
        return self.row_resolver.table_style

    def from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self.table_style is None:
            return NotFound(self, path)
        return self.from_style_inheritance(self.table_style, path, optional)
