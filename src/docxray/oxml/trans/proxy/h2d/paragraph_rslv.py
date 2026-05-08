from __future__ import annotations

from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import SE_StyleType

from .resolver import Resolver


class ParagraphResolver(Resolver[Paragraph]):
    @cached_property
    def para_style(self) -> ParagraphStyle | None:
        path = self._prop_path("val", "pPr.pStyle")
        style_id: str | None = safe_get_prop(self._proxy.element, path)
        if style_id is None:
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        if self.para_style is None:
            return None
        return self._from_style_inheritance(self.para_style, property_path)


class _NumberingResolver(Resolver[Paragraph]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
