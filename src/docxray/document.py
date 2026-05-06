"""|Document| and closely related objects."""

from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.blkcntnr import BlockItemContainer
from docxray.oxml.transitional.document import CT_Body, CT_Document
from docxray.shared import ElementProxy
from docxray.table import Table
from docxray.text.paragraph import Paragraph

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart


class Document(ElementProxy[CT_Document]):
    """WordprocessingML (WML) document.

    Not intended to be constructed directly. Use :func:`docx.Document` to open or create
    a document.
    """

    @property
    def part(self) -> DocumentPart:
        return cast("DocumentPart", self._parent)

    @cached_property
    def body(self) -> Body:
        return Body(self.element.body, self)

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate each `Paragraph` or `Table` in this document in document order."""
        return self.body.iter_inner_content()


class Body(BlockItemContainer[CT_Body]):
    pass
