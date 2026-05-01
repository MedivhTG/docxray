from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

# docxray stuff
from docxray.oxml.table import CT_Tbl
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.text.run import CT_R

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart

type StoryElements = CT_R | CT_P | CT_Tbl
STORY_ELM_T = TypeVar("STORY_ELM_T", bound=StoryElements)


class BaseFormat(Generic[STORY_ELM_T]):
    def __init__(
        self, story_elm: STORY_ELM_T, document_part: DocumentPart
    ) -> None:
        self._story_elm = story_elm
        self._styles = document_part.styles_part.styles
        num_part = document_part.numbering_part
        if num_part is None:
            self._numbering = None
        else:
            self._numbering = num_part.numbering
