from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    CharacterStyle,
)
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.st.enums import (
    SE_StyleType,
    SE_Underline,
    SE_VerticalAlignRun,
)

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
    def bold(self) -> bool:
        return self._prop_val("b")

    @cached_property
    def all_caps(self) -> bool:
        return self._prop_val("caps")

    @cached_property
    def italic(self) -> bool:
        return self._prop_val("i")

    @cached_property
    def small_caps(self) -> bool:
        return self._prop_val("smallCaps")

    @cached_property
    def strike(self) -> bool:
        return self._prop_val("strike")

    @cached_property
    def vertical_align(self) -> SE_VerticalAlignRun | None:
        return self._prop_val("vertAlign")

    @cached_property
    def underline(self) -> SE_Underline | None:
        return self._prop_val("u")

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        if self.char_style is None:
            return None
        return self._from_style_inheritance(self.char_style, property_path)
