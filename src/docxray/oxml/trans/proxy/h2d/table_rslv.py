from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
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
        style_id = self._prop_val("tblStyle", only_direct=True)
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    # TODO: change for trans
    def _prop_from_tbl_look(self, prop: str) -> bool:
        path = self._prop_path(prop, f"{self._path_base}.tblLook")
        val = self._prop(
            prop, path=path, prop_can_be_none=True, only_direct=True
        )
        if isinstance(val, NotFound):
            return False
        return on_off(val)

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
        self, prop_path: PropertyPath, **kwargs: Any
    ) -> NotFound | None:
        if self.table_style is None:
            return NotFound(self, prop_path)
        return self._from_style_inheritance(self.table_style, prop_path)


class RowResolver(Resolver[Row]):
    @cached_property
    def table_resolver(self) -> TableResolver:
        return self._proxy.table.h2d._rslvr

    @cached_property
    def table_style(self) -> TableStyle | None:
        return self.table_resolver.table_style

    @cached_property
    def _cnf(self) -> WD_CNF_FORMAT | None:
        cnf = self._prop_val("cnfStyle", only_direct=True)
        if isinstance(cnf, NotFound):
            return None
        return WD_CNF_FORMAT.from_string(cnf)

    def _from_styles_hierarchy(
        self, prop_path: PropertyPath, **kwargs: Any
    ) -> NotFound | Any:
        if self.table_style is None:
            return NotFound(self, prop_path)
        return self._from_style_inheritance(self.table_style, prop_path)


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
    def _cnf_row(self) -> WD_CNF_FORMAT | None:
        return self.row_resolver._cnf

    @cached_property
    def _cnf(self) -> WD_CNF_FORMAT | None:
        cnf = self._prop_val("cnfStyle", only_direct=True)
        if isinstance(cnf, NotFound):
            return None
        return WD_CNF_FORMAT.from_string(cnf)

    def _from_styles_hierarchy(
        self, prop_path: PropertyPath, **kwargs: Any
    ) -> NotFound | Any:
        if self.table_style is None:
            return NotFound(self, prop_path)
        return self._from_style_inheritance(self.table_style, prop_path)
