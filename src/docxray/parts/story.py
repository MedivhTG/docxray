"""|StoryPart| and related objects."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, TypeVar

# docxray stuff
from docxray.enum.word import WD_STYLE_TYPE
from docxray.opc.part import XmlPart
from docxray.types import ELM_T

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart
    from docxray.styles.style import BaseStyle

STYLE_T = TypeVar("STYLE_T", bound="BaseStyle")


class StoryPart(XmlPart[ELM_T]):
    """Base class for story parts.

    A story part is one that can contain textual content, such as the document-part and
    header or footer parts. These all share content behaviors like `.paragraphs`,
    `.add_paragraph()`, `.add_table()` etc.
    """

    def get_style(
        self,
        style_id: str,
        style_type: WD_STYLE_TYPE,
        assert_style: type[STYLE_T],
    ) -> BaseStyle:
        """Return the style in this document matching `style_id`."""
        return self.document_part.get_style(style_id, style_type, assert_style)

    @cached_property
    def document_part(self) -> DocumentPart:
        """|DocumentPart| object for this package."""
        package = self.package
        assert package is not None
        return package.main_document_part
