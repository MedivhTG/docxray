from __future__ import annotations

from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_TABLE_LOOK
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    TableStyle,
)
from docxray.oxml.trans.proxy.table import Table
from docxray.oxml.trans.st.enums import SE_StyleType
from docxray.oxml.trans.table.table_props import CT_TblBorders

from .how2display import How2Display


class TableH2D(How2Display[Table]):
    @cached_property
    def row_band_size(self) -> int:
        size = self._prop_val("tblStyleRowBandSize", algorithm="style")
        if isinstance(size, NotFound):
            return 1
        return size

    @cached_property
    def col_band_size(self) -> int:
        size = self._prop_val("tblStyleColBandSize", algorithm="style")
        if isinstance(size, NotFound):
            return 1
        return size

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        mask: bytes | None = self._prop_val("tblLook", optional=True)
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)

    @cached_property
    def _tblBorders(self) -> CT_TblBorders | None:
        tblBorders_elm = self._prop("tblBorders", algorithm="both")
        if isinstance(tblBorders_elm, NotFound):
            return None
        return tblBorders_elm

    @cached_property
    def _table_style(self) -> TableStyle | None:
        style_id = self._prop_val("tblStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.TABLE,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.TABLE],
        )

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> NotFound | None:
        if self._table_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._table_style, path, optional)
