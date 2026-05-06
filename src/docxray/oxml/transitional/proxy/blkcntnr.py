"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, TypeVar

# docxray stuff
from docxray.oxml.transitional.document import CT_Body
from docxray.oxml.transitional.proxy.shared import StoryChild
from docxray.oxml.transitional.proxy.text.paragraph import Paragraph
from docxray.oxml.transitional.table.table import CT_Tc
from docxray.oxml.transitional.text.paragraph import CT_P

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.transitional.proxy.table import Table

type _BlockItemElement = CT_Body | CT_Tc

BLCK_ITEM_ELM_T = TypeVar("BLCK_ITEM_ELM_T", bound=_BlockItemElement)


class BlockItemContainer(StoryChild[BLCK_ITEM_ELM_T]):
    """Base class for proxy objects that can contain block items.

    These containers include _Body, _Cell, header, footer, footnote, endnote, comment,
    and text box objects. Provides the shared functionality to add a block item like a
    paragraph or table.
    """

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate each `Paragraph` or `Table` in this container in document order."""
        # docxray stuff
        from docxray.oxml.transitional.proxy.table import Table

        for element in self._element.inner_content_elements:
            yield (
                Paragraph(element, self)
                if isinstance(element, CT_P)
                else Table(element, self)
            )
