"""Styles object, container for all objects in the styles part."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, TypeVar, cast

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.styles import CT_Styles
from docxray.oxml.table import CT_Tbl
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.text.run import CT_R
from docxray.shared import ElementProxy
from docxray.styles.doc_dflts import DocumentDefaults
from docxray.styles.style import (
    BaseStyle,
    CharacterStyle,
    ParagraphStyle,
    StyleFactory,
    TableStyle,
)
from docxray.types import ProvidesXmlPart

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
        rPr_elm = r_elm.rPr
        if rPr_elm is None:
            return None
        rStyle_elm = rPr_elm.rStyle
        if rStyle_elm is None:
            return None
        return self.get_by_id(
            rStyle_elm.val, WD_STYLE_TYPE.CHARACTER, CharacterStyle
        )

    def para_style(self, p_elm: CT_P) -> ParagraphStyle | None:
        pPr_elm = p_elm.pPr
        if pPr_elm is None:
            return None
        pStyle_elm = pPr_elm.pStyle
        if pStyle_elm is None:
            return None
        return self.get_by_id(
            pStyle_elm.val, WD_STYLE_TYPE.PARAGRAPH, ParagraphStyle
        )

    def table_style(self, tbl_elm: CT_Tbl) -> TableStyle | None:
        tblPr_elm = tbl_elm.tblPr
        if tblPr_elm is None:
            return None
        tblStyle_elm = tblPr_elm.tblStyle
        if tblStyle_elm is None:
            return None
        return self.get_by_id(
            tblStyle_elm.val, WD_STYLE_TYPE.TABLE, TableStyle
        )

    def get_by_id(
        self,
        style_id: str,
        style_type: WD_STYLE_TYPE,
        assert_style: type[STYLE_T],
    ) -> STYLE_T:
        """Return the style of `style_type` matching `style_id`."""
        style = self._get_by_id(style_id, style_type)
        assert isinstance(style, assert_style)
        return style

    def _get_by_id(
        self, style_id: str, style_type: WD_STYLE_TYPE
    ) -> BaseStyle:
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
