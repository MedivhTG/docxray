"""|Document| and closely related objects."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.blkcntnr import BlockItemContainer
from docxray.oxml.document import CT_Document
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart


class Document(ElementProxy[CT_Document]):
    """WordprocessingML (WML) document.

    Not intended to be constructed directly. Use :func:`docx.Document` to open or create
    a document.
    """

    def __init__(self, element: CT_Document, part: DocumentPart) -> None:
        super().__init__(element, part)
        self._part = part

    @cached_property
    def body(self) -> Body:
        return Body(self.element.body, self)

    @property
    def part(self) -> DocumentPart:
        """The |DocumentPart| object of this document."""
        return self._part


class Body(BlockItemContainer[CT_Document]):
    pass
