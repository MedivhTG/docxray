from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.t.proxy.base import NotFound, StoryChild
from docxray.oxml.t.proxy.styles.style import CharacterStyle
from docxray.oxml.t.st.enums import SE_STYLE_TYPE
from docxray.oxml.t.text.run import CT_R

from .char_format import CharacterFormat
from .run_content import RunInnerContent, TxtFragment, run_inner_content

if TYPE_CHECKING:
    from .paragraph import Paragraph


class Run(StoryChild[CT_R]):
    @cached_property
    def paragraph(self) -> Paragraph:
        """Current paragraph where is run contained"""
        from .hyperlink import Hyperlink
        from .paragraph import Paragraph

        if isinstance(self._parent, Paragraph):
            return self._parent
        elif isinstance(self._parent, Hyperlink):
            return self._parent.paragraph
        return cast(Paragraph, self._parent)

    @cached_property
    def character_format(self) -> CharacterFormat:
        return CharacterFormat(self)

    @cached_property
    def raw_text(self) -> str:
        """Accumulated text from tags `<w:t>`."""
        txt = ""
        for item in self.iter_inner_content():
            if isinstance(item, TxtFragment):
                txt += item.raw
        return txt

    @cached_property
    def character_style(self) -> CharacterStyle | None:
        """Direct style applied for run."""
        style_id = self.prop("rPr.rStyle.val")
        if isinstance(style_id, NotFound):
            return None
        return self.document_part.styles.get_by_id(
            style_id, SE_STYLE_TYPE.CHARACTER, CharacterStyle
        )

    def iter_inner_content(
        self,
    ) -> Iterator[RunInnerContent]:
        for item in self.element.inner_content_items:
            yield run_inner_content(item, self)
