from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

# docxray stuff
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import (
    CharacterStyle,
    NumberingStyle,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.document import DocumentPart

DEFAULT_T = TypeVar("DEFAULT_T")
PROXY_T = TypeVar("PROXY_T")


class Resolver(Generic[PROXY_T]):
    def __init__(
        self,
        story: PROXY_T,
        document_part: DocumentPart,
        property_base: str,
    ) -> None:
        self._proxy = story
        self._document_part = document_part
        self._styles = document_part.styles_part.styles
        num_part = document_part.numbering_part
        if num_part is None:
            self._numbering = None
        else:
            self._numbering = num_part.numbering
        self._property_base = property_base

    def _prop_path(self, end_name: str, path_to_name: str) -> PropertyPath:
        return PropertyPath.base(end_name, path_to_name)

    def _prop(
        self,
        name: str,
        default: DEFAULT_T | None = None,
        path: PropertyPath | None = None,
        only_direct: bool = False,
        **kwargs: Any,
    ) -> Any | DEFAULT_T:
        path = path or self._prop_path(name, self._property_base)
        direct_val = safe_get_prop(getattr(self._proxy, "element"), path)
        if direct_val is not None:
            return direct_val
        if only_direct:
            return direct_val
        style_val = self._from_styles_hierarchy(path, **kwargs)
        if style_val is not None:
            return style_val
        return default

    def _prop_val(
        self,
        name: str,
        default: DEFAULT_T | None = None,
        only_direct: bool = False,
        **kwargs: Any,
    ) -> Any | DEFAULT_T:
        path = self._prop_path("val", f"{self._property_base}.{name}")
        return self._prop(name, default, path, only_direct, **kwargs)

    def _from_doc_dflts(self, property_path: PropertyPath) -> Any | None:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return None
        return safe_get_prop(doc_dflts.element, property_path)

    def _from_style_inheritance(
        self,
        style: CharacterStyle | NumberingStyle,
        property_path: PropertyPath,
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
