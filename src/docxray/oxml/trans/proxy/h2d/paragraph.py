from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import SE_OnOff1, SE_StyleType

from .how2display import How2Display


class ParagraphH2D(How2Display[Paragraph]):
    @cached_property
    def cell(self) -> Cell | None:
        container = self._proxy.container
        if isinstance(container, Cell):
            return container
        return None

    @cached_property
    def _para_style(self) -> ParagraphStyle | None:
        style_id = self._prop_val("pStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    def _prop_val_run_toggled(
        self, name: str
    ) -> NotFound | None | bool | SE_OnOff1:
        path = self._prop_path("val", f"rPr.{name}")
        return self._from_styles_hierarchy(path, True)

    def _prop_val_run(self, name: str, optional: bool = True) -> Any:
        path = self._prop_path("val", f"rPr.{name}")
        return self._from_styles_hierarchy(path, optional)

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._para_style is None:
            return NotFound(self, path)
        return self._from_style_inheritance(self._para_style, path, optional)
