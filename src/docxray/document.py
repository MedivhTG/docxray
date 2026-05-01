"""|Document| and closely related objects."""

from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.blkcntnr import BlockItemContainer
from docxray.oxml.document import CT_Body, CT_Document
from docxray.shared import PartProxy
from docxray.table import Table
from docxray.text.paragraph import Paragraph

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart


class Document(PartProxy[CT_Document, "DocumentPart"]):
    """WordprocessingML (WML) document.

    Not intended to be constructed directly. Use :func:`docx.Document` to open or create
    a document.
    """

    def __init__(self, element: CT_Document, part: DocumentPart) -> None:
        super().__init__(element)
        self._part = part

    @cached_property
    def body(self) -> Body:
        return Body(self.element.body, self)

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate each `Paragraph` or `Table` in this document in document order."""
        return self.body.iter_inner_content()


class Body(BlockItemContainer[CT_Body, Document]):
    pass
