"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

from collections.abc import Iterator
from typing import TYPE_CHECKING, TypeVar

# docxray stuff
from docxray.oxml.document import CT_Body
from docxray.oxml.table import CT_Tc
from docxray.oxml.text.paragraph import CT_P
from docxray.shared import ElementProxy
from docxray.table import Table
from docxray.text.paragraph import Paragraph

if TYPE_CHECKING:
    # docxray stuff
    from docxray.document import Document


type _BlockItemElement = CT_Body | CT_Tc
type _Parent = "Document | Table"

BLCK_ITEM_ELM_T = TypeVar("BLCK_ITEM_ELM_T", bound=_BlockItemElement)
PARENT_T = TypeVar("PARENT_T", bound=_Parent)


class BlockItemContainer(ElementProxy[BLCK_ITEM_ELM_T, PARENT_T]):
    """Base class for proxy objects that can contain block items.

    These containers include _Body, _Cell, header, footer, footnote, endnote, comment,
    and text box objects. Provides the shared functionality to add a block item like a
    paragraph or table.
    """

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        """Generate each `Paragraph` or `Table` in this container in document order."""
        for element in self._element.inner_content_elements:
            yield (
                Paragraph(element, self)
                if isinstance(element, CT_P)
                else Table(element, self)
            )
