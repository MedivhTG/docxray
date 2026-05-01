"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

# docxray stuff
from docxray.oxml.document import CT_Body
from docxray.shared import StoryChild
from docxray.types import ELM_T, ProvidesStoryPart

type BlockItemElement = CT_Body


class BlockItemContainer(StoryChild[ELM_T]):
    """Base class for proxy objects that can contain block items.

    These containers include _Body, _Cell, header, footer, footnote, endnote, comment,
    and text box objects. Provides the shared functionality to add a block item like a
    paragraph or table.
    """

    def __init__(
        self, element: BlockItemElement, parent: ProvidesStoryPart[ELM_T]
    ) -> None:
        super().__init__(parent)
        self._element = element
