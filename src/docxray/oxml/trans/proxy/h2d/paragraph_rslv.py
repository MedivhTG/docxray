from __future__ import annotations

from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.compute import on_off
from docxray.oxml.trans.proxy.h2d.table_rslv import TableResolver
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import SE_StyleType

from .resolver import Resolver


class ParagraphResolver(Resolver[Paragraph]):
    @cached_property
    def para_style(self) -> ParagraphStyle | None:
        style_id = self._prop_val("pStyle", direct_only=True)
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    @cached_property
    def table_resolver(self) -> TableResolver | None:
        container = self._proxy.container
        if isinstance(container, Cell):
            return container.h2d._rslvr.table_resolver
        return None

    # --- Properties for Run
    def _prop_val_for_rpr(self, name: str, toggled: bool) -> Any:
        path = self._prop_path("val", f"rPr.{name}")
        val = self._from_styles_hierarchy(path, toggled)
        if toggled:
            if isinstance(val, NotFound):
                return val
            return on_off(val)
        return val

    @cached_property
    def i(self) -> bool | NotFound:
        return self._prop_val_for_rpr("i", True)

    @cached_property
    def b(self) -> bool | NotFound:
        return self._prop_val_for_rpr("b", True)

    @cached_property
    def caps(self) -> bool | NotFound:
        return self._prop_val_for_rpr("caps", True)

    @cached_property
    def smallCaps(self) -> bool | NotFound:
        return self._prop_val_for_rpr("smallCaps", True)

    @cached_property
    def strike(self) -> bool | NotFound:
        return self._prop_val_for_rpr("strike", True)

    # ---

    def _from_styles_hierarchy(
        self,
        prop_path: PropertyPath,
        prop_optional: bool = False,
        **kwargs: Any,
    ) -> Any:
        if self.para_style is None:
            return NotFound(self, prop_path)
        return self._from_style_inheritance(
            self.para_style, prop_path, prop_optional
        )


class _NumberingResolver(Resolver[Paragraph]):
    def _from_styles_hierarchy(
        self,
        prop_path: PropertyPath,
        prop_optional: bool = False,
        **kwargs: Any,
    ) -> Any:
        return NotFound(self, prop_path)
