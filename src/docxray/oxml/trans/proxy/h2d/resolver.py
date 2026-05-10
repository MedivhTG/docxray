from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import (
    CharacterStyle,
    NumberingStyle,
    TableStyle,
)
from docxray.oxml.trans.styles import CT_TblStylePr

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
        self._path_base = property_base

    def _prop_path(
        self, end_name: str, path_to_name: str = ""
    ) -> PropertyPath:
        return PropertyPath.base(end_name, path_to_name)

    def _prop(
        self,
        name: str,
        can_be_none: bool = False,
        direct_only: bool = False,
        path: PropertyPath | None = None,
        **kwargs: Any,
    ) -> Any:
        path = path or self._prop_path(name, self._path_base)
        direct_val = safe_get_prop(
            getattr(self._proxy, "element"), path, can_be_none
        )
        if isinstance(direct_val, NotFound):
            if direct_only:
                return direct_val
            style_val = self._from_styles_hierarchy(path, **kwargs)
            return style_val
        if not isinstance(direct_val, NotFound):
            return direct_val
        if direct_only:
            return direct_val
        style_val = self._from_styles_hierarchy(path, **kwargs)
        return style_val

    def _prop_val(
        self,
        name: str,
        can_be_none: bool = False,
        direct_only: bool = False,
        **kwargs: Any,
    ) -> Any:
        path = self._prop_path("val", f"{self._path_base}.{name}")
        return self._prop(name, can_be_none, direct_only, path, **kwargs)

    def _table_style_props(
        self, table_style: TableStyle, cnf_flags: WD_CNF_FORMAT
    ) -> list[CT_TblStylePr]:
        props = []
        for flag in WD_CNF_FORMAT.ordered_flags():
            if cnf_flags & flag:
                tblStylePr_elm = table_style.bitwise_table_style_property(flag)
                if tblStylePr_elm is not None:
                    props.append(tblStylePr_elm)
        if table_style.wholeTable:
            props.append(table_style.wholeTable)
        return props

    def _from_doc_dflts(
        self, property_path: PropertyPath, prop_can_be_none: bool = False
    ) -> NotFound | Any:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return NotFound(self._styles, property_path)
        return safe_get_prop(
            doc_dflts.element, property_path, prop_can_be_none
        )

    def _from_style_inheritance(
        self,
        style: CharacterStyle | NumberingStyle,
        property_path: PropertyPath,
        prop_can_be_none: bool = False,
    ) -> NotFound | Any:
        val = NotFound(style, property_path)
        while isinstance(val, NotFound):
            val = safe_get_prop(style.element, property_path, prop_can_be_none)
            base_style = self._styles.base_style(style)
            if not isinstance(base_style, style.__class__):
                return val
            style = base_style
        return val

    @abstractmethod
    def _from_styles_hierarchy(
        self, prop_path: PropertyPath, **kwargs: Any
    ) -> NotFound | Any: ...
