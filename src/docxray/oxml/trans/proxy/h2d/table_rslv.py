from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    TableStyle,
)
from docxray.oxml.trans.proxy.table import Cell, Row, Table
from docxray.oxml.trans.st.enums import SE_StyleType

from .resolver import Resolver


class TableResolver(Resolver[Table]):
    @cached_property
    def table_style(self) -> TableStyle | None:
        path = self._prop_path("val", "tblPr.tblStyle")
        style_id: str | None = safe_get_prop(self._proxy.element, path)
        if style_id is None:
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    def _prop_from_tbl_look(self, prop: str) -> bool:
        path = self._prop_path(prop, f"{self._path_base}.tblLook")
        return self._prop(prop, False, path, True)

    @cached_property
    def first_row_show(self) -> bool:
        return self._prop_from_tbl_look("firstRow")

    @cached_property
    def last_row_show(self) -> bool:
        return self._prop_from_tbl_look("lastRow")

    @cached_property
    def first_col_show(self) -> bool:
        return self._prop_from_tbl_look("firstColumn")

    @cached_property
    def last_col_show(self) -> bool:
        return self._prop_from_tbl_look("lastColumn")

    @cached_property
    def no_horizontal_lines(self) -> bool:
        return self._prop_from_tbl_look("noHBand")

    @cached_property
    def no_vertical_lines(self) -> bool:
        return self._prop_from_tbl_look("noVBand")

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        if self.table_style is None:
            return None
        return self._from_style_inheritance(self.table_style, property_path)


class RowResolver(Resolver[Row]):
    @cached_property
    def table_resolver(self) -> TableResolver:
        return self._proxy.table.h2d._rslvr

    @cached_property
    def table_style(self) -> TableStyle | None:
        return self.table_resolver.table_style

    @cached_property
    def cnf(self) -> WD_CNF_FORMAT | None:
        return self._prop_val("cnfStyle", only_direct=True)

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        if self.table_style is None:
            return None
        return self._from_style_inheritance(self.table_style, property_path)


class CellResolver(Resolver[Cell]):
    @cached_property
    def row_resolver(self) -> RowResolver:
        return self._proxy.row.h2d._rslvr

    @cached_property
    def table_resolver(self) -> TableResolver:
        return self.row_resolver.table_resolver

    @cached_property
    def table_style(self) -> TableStyle | None:
        return self.row_resolver.table_style

    @cached_property
    def row_cnf(self) -> WD_CNF_FORMAT | None:
        return self.row_resolver.cnf

    @cached_property
    def cnf(self) -> WD_CNF_FORMAT | None:
        return self._prop_val("cnfStyle", only_direct=True)

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        if self.table_style is None:
            return None
        return self._from_style_inheritance(self.table_style, property_path)
