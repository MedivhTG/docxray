from __future__ import annotations

from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.h2d.table_rslv import TableResolver
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import SE_OnOff1, SE_StyleType

from .resolver import Resolver


class ParagraphResolver(Resolver[Paragraph]):
    @cached_property
    def para_style(self) -> ParagraphStyle | None:
        style_id = self.prop_val("pStyle")
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

    def _prop_val_run_toggled(
        self, name: str
    ) -> NotFound | None | bool | SE_OnOff1:
        path = self.prop_path("val", f"rPr.{name}")
        return self.from_styles_hierarchy(path, True)

    def from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self.para_style is None:
            return NotFound(self, path)
        return self.from_style_inheritance(self.para_style, path, optional)


class _NumberingResolver(Resolver[Paragraph]):
    def from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        return NotFound(self, path)
