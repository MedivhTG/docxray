"""|Document| and closely related objects."""

from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.document import CT_Body, CT_Document
from docxray.oxml.trans.h2d.list_view import ListViewInterrupted

from .blkcntnr import BlockItemContainer
from .shared import ElementProxy
from .table import Table
from .text.paragraph import Paragraph

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.document import DocumentPart


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

    def iter_inner_content_with_lists(
        self,
    ) -> Iterator[Paragraph | Table | ListViewInterrupted]:
        return self.body.iter_inner_content_with_lists()


class Body(BlockItemContainer[CT_Body]):
    pass
