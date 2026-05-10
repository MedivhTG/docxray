from functools import cached_property
from typing import Any, cast

# docxray stuff
from docxray.oxml.trans.proxy.h2d.paragraph_rslv import ParagraphResolver
from docxray.oxml.trans.proxy.h2d.table_rslv import TableResolver
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
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
        style_id = self._prop_val("rStyle", direct_only=True)
        if isinstance(style_id, NotFound):
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
    def table_resolver(self) -> TableResolver | None:
        return self.paragraph_resolver.table_resolver

    @cached_property
    def para_style(self) -> ParagraphStyle | None:
        return self.paragraph_resolver.para_style

    @cached_property
    def i(self) -> bool | NotFound:
        return self._prop_val("i", True, True)

    @cached_property
    def b(self) -> bool | NotFound:
        return self._prop_val("b", True, True)

    @cached_property
    def caps(self) -> bool | NotFound:
        return self._prop_val("caps", True, True)

    @cached_property
    def smallCaps(self) -> bool | NotFound:
        return self._prop_val("smallCaps", True, True)

    @cached_property
    def strike(self) -> bool | NotFound:
        return self._prop_val("strike", True, True)

    def _from_styles_hierarchy(
        self,
        prop_path: PropertyPath,
        prop_optional: bool = False,
        **kwargs: Any,
    ) -> NotFound | Any:
        if self.char_style is None:
            return NotFound(self, prop_path)
        return self._from_style_inheritance(
            self.char_style, prop_path, prop_optional
        )
