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
    def para_style(self) -> ParagraphStyle:
        path = self._prop_path("val", "rPr.rStyle")
        style_id = safe_get_prop(self._proxy.element, path)
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    # @cached_property
    # def in_list(self) -> bool:
    #     num_path = self._prop_path("numPr", "pPr")
    #     numPr: CT_NumPr | None = safe_get_prop(self._proxy.element, num_path)
    #     if numPr is not None:
    #         return True
    #     para_style = self.para_style
    #     if para_style is None:
    #         return False
    #     numPr = None
    #     while numPr is None:
    #         numPr = safe_get_prop(
    #             para_style.element,
    #             self._prop_path("numPr", f"{self._property_base}"),
    #         )
    #         if numPr is not None:
    #             return True
    #         base_style = self._styles.base_style(para_style)
    #         if not isinstance(base_style, para_style.__class__):
    #             return False
    #         para_style = base_style

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return self._from_style_inheritance(self.para_style, property_path)


class _NumberingResolver(Resolver[Paragraph]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
