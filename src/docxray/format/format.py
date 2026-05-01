from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

# docxray stuff
from docxray.format.property_path import PropertyPath, safe_get_prop
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
        self,
        story_elm: STORY_ELM_T,
        document_part: DocumentPart,
        property_base: str,
    ) -> None:
        self._story_elm = story_elm
        self._styles = document_part.styles_part.styles
        num_part = document_part.numbering_part
        if num_part is None:
            self._numbering = None
        else:
            self._numbering = num_part.numbering
        self._property_base = property_base

    def _rslv_prop(self, name: str, **kwargs: Any) -> Any | None:
        path = PropertyPath.base(name, self._property_base)
        direct = safe_get_prop(self._story_elm, path)
        if direct is None:
            return self._rslv_from_styles(path, **kwargs)
        return direct

    def _rslv_from_doc_dflts(self, property_path: PropertyPath) -> Any | None:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return None
        return safe_get_prop(doc_dflts.element, property_path)

    @abstractmethod
    def _rslv_from_styles(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None: ...
