"""Styles object, container for all objects in the styles part."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.oxml.styles import CT_Styles
from docxray.shared import PartProxy
from docxray.styles.style import BaseStyle, StyleFactory

STYLE_T = TypeVar("STYLE_T", bound=BaseStyle)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.styles import StylesPart  # noqa: F401


class Styles(PartProxy[CT_Styles, "StylesPart"]):
    """Provides access to the styles defined in a document."""

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
        style = self.element.get_by_id(style_id) if style_id else None
        if style is None or style.type != style_type:
            msg = f"No such style by id {style_id}"
            raise ValueError(msg)
        return StyleFactory(style, self.part)
