from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

# docxray stuff
from docxray.enum.table import WD_CNF_FORMAT
from docxray.oxml.table import CT_Row, CT_Tbl, CT_Tc
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.text.run import CT_R
from docxray.oxml.xmlchemy import OxmlElement
from docxray.resolver.exceptions import ResolveError
from docxray.shared import PropertyPath, safe_get_prop
from docxray.styles.style import CharacterStyle, TableStyle

if TYPE_CHECKING:
    # docxray stuff
    from docxray.parts.document import DocumentPart

type StoryElements = CT_R | CT_P | CT_Tbl
STORY_ELM_T = TypeVar("STORY_ELM_T", bound=StoryElements)
PARENT_T = TypeVar("PARENT_T", bound=OxmlElement)


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

    def _elm_parent(
        self, elm: OxmlElement, parent_type: type[PARENT_T]
    ) -> PARENT_T:
        parent = elm.getparent(parent_type)
        if not isinstance(parent, parent_type):
            msg = f"Cannot get from {elm} parent of derived type {parent_type}"
            raise ResolveError(msg)
        return parent

    def _from_doc_dflts(self, property_path: PropertyPath) -> Any | None:
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return None
        return safe_get_prop(doc_dflts.element, property_path)

    def _from_char_style(
        self, r_elm: CT_R, property_path: PropertyPath
    ) -> Any | None:
        char_style = self._styles.char_style(r_elm)
        if char_style is None:
            return None
        return self._from_style_inheritance(char_style, property_path)

    def _from_para_style(
        self, p_elm: CT_P, property_path: PropertyPath
    ) -> Any | None:
        para_style = self._styles.para_style(p_elm)
        if para_style is None:
            return None
        return self._from_style_inheritance(para_style, property_path)

    def _from_table_style(
        self, tbl_elm: CT_Tbl, property_path: PropertyPath
    ) -> Any | None:
        table_style = self._styles.table_style(tbl_elm)
        if table_style is None:
            return None
        return self._from_style_inheritance(table_style, property_path)

    def _from_table_style_hierarchy(
        self, tc_elm: CT_Tc, property_path: PropertyPath
    ) -> Any | None:
        tr_elm = self._elm_parent(tc_elm, CT_Row)
        tbl_elm = self._elm_parent(tr_elm, CT_Tbl)
        table_val = self._from_table_style(tbl_elm, property_path)
        if table_val is not None:
            return table_val

        cnf_flags = None
        tr_cnf_flags: WD_CNF_FORMAT | None = safe_get_prop(
            tr_elm, PropertyPath.base("val", "trPr.cnfStyle")
        )
        tc_cnf_flags: WD_CNF_FORMAT | None = safe_get_prop(
            tc_elm, PropertyPath.base("val", "tcPr.cnfStyle")
        )
        if tr_cnf_flags is not None:
            cnf_flags = tr_cnf_flags
        if tc_cnf_flags is not None:
            if cnf_flags is None:
                cnf_flags = tc_cnf_flags
            else:
                cnf_flags |= tc_cnf_flags
        if cnf_flags is None:
            return None
        table_style = self._styles.table_style(tbl_elm)
        if table_style is None:
            msg = f"Table style not found for {tc_elm} when cnf_flags were derived inside or in upper parents"
            raise ResolveError(msg)
        return self._from_cnf_style(table_style, cnf_flags, property_path)

    def _from_cnf_style(
        self,
        table_style: TableStyle,
        cnf_flags: WD_CNF_FORMAT,
        property_path: PropertyPath,
    ) -> Any | None:
        for flag in WD_CNF_FORMAT.ordered_flags():
            if cnf_flags & flag:
                tblStylePr_elm = table_style.bitwise_table_style_property(flag)
                if tblStylePr_elm is None:
                    continue
                cnf_val = safe_get_prop(tblStylePr_elm, property_path)
                if cnf_val is None:
                    continue
                return cnf_val
        return None

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
