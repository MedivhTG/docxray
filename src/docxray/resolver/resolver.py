from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

# docxray stuff
from docxray.oxml.table import CT_Tbl
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.text.run import CT_R
from docxray.oxml.xmlchemy import OxmlElement
from docxray.resolver.property_path import PropertyPath, safe_get_prop
from docxray.styles.style import CharacterStyle

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart

type StoryElements = CT_R | CT_P | CT_Tbl
STORY_ELM_T = TypeVar("STORY_ELM_T", bound=StoryElements)
ANCESTOR_T = TypeVar("ANCESTOR_T", bound=OxmlElement)


class ResolveError(Exception):
    pass


class BaseResolver(Generic[STORY_ELM_T]):
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

    def _prop(self, name: str, **kwargs: Any) -> Any | None:
        path = PropertyPath.base(name, self._property_base)
        direct = safe_get_prop(self._story_elm, path)
        if direct is None:
            return self._from_styles_hierarchy(path, **kwargs)
        return direct

    def _elm_ancestor(
        self, elm: OxmlElement, ancestor_type: type[ANCESTOR_T]
    ) -> ANCESTOR_T:
        ancestor = elm.ancestor(ancestor_type)
        if ancestor is None:
            msg = f"Ancestor of type {ancestor_type} not found for {elm}"
            raise ResolveError(msg)
        return ancestor

    def _from_doc_dflts(self, property_path: PropertyPath) -> Any | None:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return None
        return safe_get_prop(doc_dflts.element, property_path)

    def _from_char_style(
        self, story_elm: CT_R, property_path: PropertyPath
    ) -> Any | None:
        char_style = self._styles.char_style(story_elm)
        if char_style is None:
            return None
        return self._from_style_inheritance(char_style, property_path)

    def _from_para_style(
        self, story_elm: CT_P, property_path: PropertyPath
    ) -> Any | None:
        para_style = self._styles.para_style(story_elm)
        if para_style is None:
            return None
        return self._from_style_inheritance(para_style, property_path)

    def _from_style_inheritance(
        self, style: CharacterStyle, property_path: PropertyPath
    ) -> Any | None:
        val = None
        while val is None:
            val = safe_get_prop(style.element, property_path)
            base_style = self._styles.base_style(style)
            if not isinstance(base_style, style.__class__):
                return val
            style = base_style
        return val

    @abstractmethod
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None: ...
