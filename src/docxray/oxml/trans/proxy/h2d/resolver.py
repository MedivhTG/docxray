from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar

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

type ResolveAlgorithm = Literal["direct", "style", "both"]


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

    def prop_path(self, name: str, path_base: str = "") -> PropertyPath:
        return PropertyPath.base(name, path_base)

    def prop_direct(self, path: PropertyPath, optional: bool = False) -> Any:
        elm = getattr(self._proxy, "element")
        return safe_get_prop(elm, path, optional)

    def prop_style(self, path: PropertyPath, optional: bool = False) -> Any:
        return self.from_styles_hierarchy(path, optional)

    def prop_both(self, path: PropertyPath, optional: bool = False) -> Any:
        elm = getattr(self._proxy, "element")
        direct_val = safe_get_prop(elm, path, optional)
        if isinstance(direct_val, NotFound):
            return self.from_styles_hierarchy(path, optional)
        return direct_val

    def prop(
        self,
        name_or_path: str | PropertyPath,
        optional: bool = False,
        algorithm: ResolveAlgorithm = "direct",
        **kwargs: Any,
    ) -> Any:
        if isinstance(name_or_path, PropertyPath):
            path = name_or_path
        else:
            path = self.prop_path(name_or_path, self._path_base)
        match algorithm:
            case "direct":
                return self.prop_direct(path, optional)
            case "style":
                return self.prop_style(path, optional)
            case "both":
                return self.prop_both(path, optional)

    def prop_val(
        self,
        name: str,
        optional: bool = False,
        algorithm: ResolveAlgorithm = "direct",
    ) -> Any:
        path = self.prop_path("val", f"{self._path_base}.{name}")
        return self.prop(path, optional, algorithm)

    def table_style_props(
        self, table_style: TableStyle, cnf: WD_CNF_FORMAT
    ) -> list[CT_TblStylePr]:
        props = []
        for flag in WD_CNF_FORMAT.ordered_flags():
            format = cnf & flag
            if format:
                tblStylePr_elm = table_style.bitwise_tbl_style_prop(flag)
                if tblStylePr_elm is not None:
                    props.append(tblStylePr_elm)
        if table_style.wholeTable:
            props.append(table_style.wholeTable)
        return props

    def from_doc_dflts(
        self, path: PropertyPath, optional: bool = False
    ) -> Any:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return NotFound(self._styles, path)
        return safe_get_prop(doc_dflts.element, path, optional)

    def from_style_inheritance(
        self,
        style: CharacterStyle | NumberingStyle,
        path: PropertyPath,
        optional: bool = False,
    ) -> Any:
        val = NotFound(style, path)
        while isinstance(val, NotFound):
            val = safe_get_prop(style.element, path, optional)
            base_style = self._styles.base_style(style)
            if not isinstance(base_style, style.__class__):
                return val
            style = base_style
        return val

    @abstractmethod
    def from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any: ...
