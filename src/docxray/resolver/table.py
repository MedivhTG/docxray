from functools import cached_property
from typing import Any

# docxray stuff
from docxray.enum.word import WD_CNF_FORMAT
from docxray.oxml.transitional.simple_types.st.enums import SE_Border
from docxray.oxml.transitional.table.table import CT_Row, CT_Tbl, CT_Tc
from docxray.resolver.exceptions import ResolveError
from docxray.resolver.resolver import BaseResolver
from docxray.shared import PropertyPath, safe_get_prop


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
        return self._prop_border_val("top")

    @cached_property
    def bottom(self) -> SE_Border | None:
        return self._prop_border_val("bottom")

    @cached_property
    def left(self) -> SE_Border | None:
        return self._prop_border_val("left")

    @cached_property
    def right(self) -> SE_Border | None:
        return self._prop_border_val("right")

    @cached_property
    def inside_horizontal(self) -> SE_Border | None:
        return self._prop_border_val("insideH")

    @cached_property
    def inside_vertical(self) -> SE_Border | None:
        return self._prop_border_val("insideV")

    def _prop_border_val(self, name: str) -> SE_Border | None:
        path = self._prop_val_path(name, f"{self._property_base}.tcBorders")
        return self._prop_val(name, path=path, is_border=True)

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        is_border: bool = kwargs.pop("is_border", False)
        if is_border:
            return self._from_table_style_hierarchy_bordered(
                self._elm, property_path
            )
        return self._from_table_style_hierarchy(self._elm, property_path)

    def _from_table_style_hierarchy_bordered(
        self, tc_elm: CT_Tc, property_path: PropertyPath
    ) -> Any | None:
        tr_elm = self._elm_parent(tc_elm, CT_Row)
        tbl_elm = self._elm_parent(tr_elm, CT_Tbl)

        cell_val = self._from_table_style(tbl_elm, property_path)
        if cell_val is not None:
            return cell_val
        table_val = self._from_table_style(
            tbl_elm,
            self._prop_val_path(property_path.prop, f"tblPr.tblBorders"),
        )
        if table_val is not None:
            return table_val
        cnf_flags = None
        tr_cnf_flags: WD_CNF_FORMAT | None = safe_get_prop(
            tr_elm, PropertyPath.base("val", "trPr.cnfStyle")
        )
        tc_cnf_flags: WD_CNF_FORMAT | None = safe_get_prop(
            tc_elm, PropertyPath.base("val", "tcPr.cnfStyle")
        )
        if tr_cnf_flags is not None:
            cnf_flags = tr_cnf_flags
        if tc_cnf_flags is not None:
            if cnf_flags is None:
                cnf_flags = tc_cnf_flags
            else:
                cnf_flags |= tc_cnf_flags
        if cnf_flags is None:
            return None
        table_style = self._styles.table_style(tbl_elm)
        if table_style is None:
            msg = f"Table style not found for {tc_elm} when cnf_flags were derived inside or in upper parents"
            raise ResolveError(msg)
        return self._from_cnf_style(table_style, cnf_flags, property_path)
