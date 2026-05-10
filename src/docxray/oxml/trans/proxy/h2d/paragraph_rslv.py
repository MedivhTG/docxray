from __future__ import annotations

from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
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
        style_id = self._prop_val("pStyle", direct_only=True)
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    def _from_styles_hierarchy(
        self, prop_path: PropertyPath, **kwargs: Any
    ) -> NotFound | Any:
        if self.para_style is None:
            return NotFound(self, prop_path)
        return self._from_style_inheritance(self.para_style, prop_path)


class _NumberingResolver(Resolver[Paragraph]):
    def _from_styles_hierarchy(
        self, prop_path: PropertyPath, **kwargs: Any
    ) -> NotFound | Any:
        return NotFound(self, prop_path)
