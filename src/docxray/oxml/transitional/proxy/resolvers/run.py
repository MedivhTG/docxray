from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.transitional.proxy.shared import PropertyPath
from docxray.oxml.transitional.simple_types.enums import (
    SE_Underline,
    SE_VerticalAlignRun,
)
from docxray.oxml.transitional.table.table import CT_Tc
from docxray.oxml.transitional.text.paragraph import CT_P
from docxray.oxml.transitional.text.run import CT_R

from .resolver import BaseResolver


class RunResolver(BaseResolver[CT_R]):
    @cached_property
    def bold(self) -> bool:
        return self._prop_toggled("b")

    @cached_property
    def all_caps(self) -> bool:
        return self._prop_toggled("caps")

    @cached_property
    def italic(self) -> bool:
        return self._prop_toggled("i")

    @cached_property
    def small_caps(self) -> bool:
        return self._prop_toggled("smallCaps")

    @cached_property
    def strike(self) -> bool:
        return self._prop_toggled("strike")

    @cached_property
    def vertical_align(self) -> SE_VerticalAlignRun | None:
        return self._prop_val("vertAlign")

    @cached_property
    def underline(self) -> SE_Underline | None:
        return self._prop_val("u")

    def _prop_toggled(self, name: str) -> bool:
        return self._prop_val(name, default=False, is_toggled=True)

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        is_toggled = kwargs.pop("is_toggled", False)
        if is_toggled:
            return self._from_styles_toggled(property_path)
        return self._from_styles_default(property_path)

    def _from_styles_toggled(self, property_path: PropertyPath) -> bool:
        doc_path = property_path.join_left("rPrDefault")
        doc_val = self._from_doc_dflts(doc_path)
        if doc_val:
            return True
        char_val = bool(self._from_char_style(self._elm, property_path))
        p_elm = self._elm_parent(self._elm, CT_P)
        para_val = bool(self._from_para_style(p_elm, property_path))
        tc_elm = p_elm.getparent(CT_Tc)
        if not isinstance(tc_elm, CT_Tc):
            return para_val ^ char_val
        table_val = bool(
            self._from_table_style_hierarchy(tc_elm, property_path)
        )
        return para_val ^ char_val ^ table_val

    def _from_styles_default(self, property_path: PropertyPath) -> Any | None:
        char_val = self._from_char_style(self._elm, property_path)
        if char_val is not None:
            return char_val
        p_elm = self._elm_parent(self._elm, CT_P)
        para_val = self._from_para_style(p_elm, property_path)
        if para_val is not None:
            return para_val
        tc_elm = p_elm.getparent(CT_Tc)
        if not isinstance(tc_elm, CT_Tc):
            return self._from_doc_dflts(property_path)
        table_val = self._from_table_style_hierarchy(tc_elm, property_path)
        if table_val is not None:
            return None
        return self._from_doc_dflts(property_path)
