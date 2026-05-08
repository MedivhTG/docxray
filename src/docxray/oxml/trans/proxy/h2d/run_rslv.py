from functools import cached_property
from typing import Any, cast

# docxray stuff
from docxray.oxml.trans.proxy.h2d.paragraph_rslv import ParagraphResolver
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    CharacterStyle,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.st.enums import SE_StyleType

from .resolver import Resolver


class RunResolver(Resolver[Run]):
    @cached_property
    def char_style(self) -> CharacterStyle | None:
        path = self._prop_path("val", "rPr.rStyle")
        style_id: str | None = safe_get_prop(self._proxy.element, path)
        if style_id is None:
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.CHARACTER,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.CHARACTER],
        )

    @cached_property
    def paragraph(self) -> Paragraph:
        return cast("Paragraph", self._proxy._parent)

    @cached_property
    def paragraph_resolver(self) -> ParagraphResolver:
        return self.paragraph.h2d._rslvr

    @cached_property
    def para_style(self) -> ParagraphStyle | None:
        return self.paragraph_resolver.para_style

    @cached_property
    def i(self) -> bool | None:
        return self._prop_val("i")

    @cached_property
    def b(self) -> bool | None:
        return self._prop_val("b")

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        if self.char_style is None:
            return None
        return self._from_style_inheritance(self.char_style, property_path)
