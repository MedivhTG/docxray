from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, cast

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

PROXY_T = TypeVar("PROXY_T")

type ResolveAlgorithm = Literal["direct", "style", "both"]


class How2Display(Generic[PROXY_T]):
    def __init__(
        self,
        story: PROXY_T,
        document_part: DocumentPart,
        property_base: str,
    ) -> None:
        self._proxy = story
        self._document_part = document_part
        self._styles = document_part.styles
        self._settings = document_part.settings_part.settings
        num_part = document_part.numbering_part
        if num_part is None:
            self._numbering = None
        else:
            self._numbering = num_part.numbering
        self._path_base = property_base

    def _prop_path(self, name: str, path_base: str = "") -> PropertyPath:
        return PropertyPath.base(name, path_base)

    def _prop_direct(self, path: PropertyPath, optional: bool = False) -> Any:
        elm = getattr(self._proxy, "element")
        return safe_get_prop(elm, path, optional)

    def _prop_style(self, path: PropertyPath, optional: bool = False) -> Any:
        return self._from_styles_hierarchy(path, optional)

    def _prop_both(self, path: PropertyPath, optional: bool = False) -> Any:
        elm = getattr(self._proxy, "element")
        direct_val = safe_get_prop(elm, path, optional)
        if isinstance(direct_val, NotFound):
            return self._from_styles_hierarchy(path, optional)
        return direct_val

    def _prop(
        self,
        name_or_path: str | PropertyPath,
        optional: bool = False,
        algorithm: ResolveAlgorithm = "direct",
    ) -> Any:
        if isinstance(name_or_path, PropertyPath):
            path = name_or_path
        else:
            path = self._prop_path(name_or_path, self._path_base)
        match algorithm:
            case "direct":
                return self._prop_direct(path, optional)
            case "style":
                return self._prop_style(path, optional)
            case "both":
                return self._prop_both(path, optional)

    def _prop_val(
        self,
        name_or_path: str | PropertyPath,
        optional: bool = False,
        algorithm: ResolveAlgorithm = "direct",
    ) -> Any:
        path = (
            name_or_path
            if isinstance(name_or_path, PropertyPath)
            else self._prop_path("val", f"{self._path_base}.{name_or_path}")
        )
        return self._prop(path, optional, algorithm)

    def _table_style_props(
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

    def _from_tbl_style_hierarchy(
        self,
        tbl_style_props_deep: list[tuple[TableStyle, list[CT_TblStylePr]]],
        path: PropertyPath,
        optional: bool = False,
    ) -> tuple[Any, TableStyle | CT_TblStylePr | None]:
        style_direct_val = NotFound(self, path)
        found_in_style = None
        for tbl_style, tbl_style_props in tbl_style_props_deep:
            if isinstance(style_direct_val, NotFound):
                style_direct_val = safe_get_prop(
                    tbl_style.element, path, optional
                )
                found_in_style = tbl_style
            tbl_val, tbl_style_prop = self._from_tbl_style_props(
                tbl_style_props, path, optional
            )
            if not isinstance(tbl_val, NotFound):
                return tbl_val, cast("CT_TblStylePr", tbl_style_prop)
        return style_direct_val, found_in_style

    def _from_tbl_style_props(
        self,
        table_style_props: list[CT_TblStylePr],
        path: PropertyPath,
        optional: bool = False,
    ) -> tuple[Any, CT_TblStylePr | None]:
        for tbl_style_prop in table_style_props:
            table_val = safe_get_prop(tbl_style_prop, path, optional)
            if isinstance(table_val, NotFound):
                continue
            return table_val, tbl_style_prop
        return NotFound(table_style_props, path), None

    def _from_doc_dflts(
        self, path: PropertyPath, optional: bool = False
    ) -> Any:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return NotFound(self._styles, path)
        return safe_get_prop(doc_dflts.element, path, optional)

    def _from_style_inheritance(
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
    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any: ...
