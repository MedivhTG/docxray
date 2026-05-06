from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import PropertyPath
from docxray.oxml.trans.st.enums import SE_Border
from docxray.oxml.trans.table.table import CT_Row, CT_Tbl, CT_Tc

from .resolver import BaseResolver


class TableResolver(BaseResolver[CT_Tbl]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class RowResolver(BaseResolver[CT_Row]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class CellResolver(BaseResolver[CT_Tc]):
    @cached_property
    def top(self) -> SE_Border | None:
        return self._prop_val_border("top")

    @cached_property
    def bottom(self) -> SE_Border | None:
        return self._prop_val_border("bottom")

    @cached_property
    def left(self) -> SE_Border | None:
        return self._prop_val_border("left")

    @cached_property
    def right(self) -> SE_Border | None:
        return self._prop_val_border("right")

    @cached_property
    def inside_horizontal(self) -> SE_Border | None:
        return self._prop_val_border("insideH")

    @cached_property
    def inside_vertical(self) -> SE_Border | None:
        return self._prop_val_border("insideV")

    def _prop_val_border(self, border_name: str) -> SE_Border | None:
        path = self._prop_path(
            "val", f"{self._property_base}.tcBorders.{border_name}"
        )
        return self._prop_val(
            border_name, path=path, is_border=True, border_name=border_name
        )

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        is_border: bool = kwargs.pop("is_border", False)
        if is_border:
            border_name = kwargs.pop("border_name", property_path.prop)
            return self._from_table_style_hierarchy_bordered(
                self._elm, property_path, border_name
            )
        return self._from_table_style_hierarchy(self._elm, property_path)

    def _from_table_style_hierarchy_bordered(
        self, tc_elm: CT_Tc, property_path: PropertyPath, border_name: str
    ) -> Any | None:

        tr_elm = self._elm_parent(tc_elm, CT_Row)
        tbl_elm = self._elm_parent(tr_elm, CT_Tbl)

        cell_val = self._from_table_style(tbl_elm, property_path)
        if cell_val is not None:
            return cell_val
        table_val = self._from_table_style(
            tbl_elm,
            self._prop_path(
                property_path.prop, f"tblPr.tblBorders.{border_name}"
            ),
        )
        if table_val is not None:
            return table_val
        return self._from_cnf_style_cell(tc_elm, property_path)

    def _foo(self):
        pass
