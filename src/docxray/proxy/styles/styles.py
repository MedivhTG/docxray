"""Styles object, container for all objects in the styles part."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, TypeVar, cast

# docxray stuff
from docxray.oxml.transitional.simple_types.enums import SE_StyleType
from docxray.oxml.transitional.styles import CT_Styles
from docxray.oxml.transitional.table.table import CT_Tbl
from docxray.oxml.transitional.text.paragraph import CT_P
from docxray.oxml.transitional.text.run import CT_R
from docxray.proxy.shared import ElementProxy, PropertyPath, safe_get_prop
from docxray.proxy.styles.doc_dflts import DocumentDefaults
from docxray.proxy.styles.style import (
    BaseStyle,
    CharacterStyle,
    NumberingStyle,
    ParagraphStyle,
    StyleFactory,
    TableStyle,
)
from docxray.proxy.types import ProvidesXmlPart

STYLE_T = TypeVar("STYLE_T", bound=BaseStyle)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.styles import StylesPart


class Styles(ElementProxy[CT_Styles]):
    """Provides access to the styles defined in a document."""

    def __init__(self, element: CT_Styles, parent: ProvidesXmlPart) -> None:
        super().__init__(element, parent)
        self._cached_styles: dict[str, BaseStyle] = {}

    @property
    def part(self) -> StylesPart:
        return cast("StylesPart", self._parent)

    @cached_property
    def document_defaults(self) -> DocumentDefaults | None:
        doc_dflts = self.element.docDefaults
        if doc_dflts is None:
            return None
        return DocumentDefaults(doc_dflts, self)

    def base_style(self, style: CharacterStyle) -> BaseStyle | None:
        basedOn = style.based_on
        if basedOn is None:
            return None
        base_style = self._cached_styles.get(basedOn)
        if base_style is None:
            new_style = style.base_style
            if new_style is None:
                return None
            self._cached_styles[basedOn] = new_style
            return new_style
        return base_style

    def char_style(self, r_elm: CT_R) -> CharacterStyle | None:
        style_id = safe_get_prop(r_elm, PropertyPath.base("val", "rPr.rStyle"))
        if style_id is None:
            return None
        return self.get_by_id(style_id, SE_StyleType.CHARACTER, CharacterStyle)

    def para_style(self, p_elm: CT_P) -> ParagraphStyle | None:
        style_id = safe_get_prop(p_elm, PropertyPath.base("val", "pPr.pStyle"))
        if style_id is None:
            return None
        return self.get_by_id(style_id, SE_StyleType.PARAGRAPH, ParagraphStyle)

    def num_style(self, style_id: str) -> NumberingStyle:
        return self.get_by_id(style_id, SE_StyleType.NUMBERING, NumberingStyle)

    def table_style(self, tbl_elm: CT_Tbl) -> TableStyle | None:
        style_id = safe_get_prop(
            tbl_elm, PropertyPath.base("val", "tblPr.tblStyle")
        )
        if style_id is None:
            return None
        return self.get_by_id(style_id, SE_StyleType.TABLE, TableStyle)

    def get_by_id(
        self,
        style_id: str,
        style_type: SE_StyleType,
        assert_style: type[STYLE_T],
    ) -> STYLE_T:
        """Return the style of `style_type` matching `style_id`."""
        style = self._get_by_id(style_id, style_type)
        assert isinstance(style, assert_style)
        return style

    def _get_by_id(self, style_id: str, style_type: SE_StyleType) -> BaseStyle:
        """Return the style of `style_type` matching `style_id`."""
        style = self._cached_styles.get(style_id)
        if style is not None:
            return style
        style = self.element.get_by_id(style_id) if style_id else None  # type: ignore[assignment]
        if style is None or style.type != style_type:
            msg = f"No such style by id {style_id}"
            raise ValueError(msg)
        style = StyleFactory(style, self.part)
        self._cached_styles[style_id] = style
        return style
