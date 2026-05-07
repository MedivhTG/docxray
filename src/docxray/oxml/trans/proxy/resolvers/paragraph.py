from functools import cached_property
from typing import Any, cast

# docxray stuff
from docxray.constants import WD_OUTLINE_LEVEL
from docxray.oxml.trans.proxy.resolvers.resolver import BaseResolver
from docxray.oxml.trans.proxy.shared import PropertyPath, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import ParagraphStyle
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.table.table import CT_Tc
from docxray.oxml.trans.text.num_props import CT_NumPr


class ParagraphResolver(BaseResolver[Paragraph]):
    @cached_property
    def outline_lvl(self) -> int:
        return self._prop_val("outlineLvl", WD_OUTLINE_LEVEL.TEXT)

    @cached_property
    def in_list(self) -> bool:
        numPr: CT_NumPr | None = safe_get_prop(
            self._proxy, PropertyPath.base("numPr", "pPr")
        )
        if numPr is not None:
            return True
        para_style = self._styles.para_style(self._proxy.element)
        if para_style is None:
            return False
        numPr = None
        while numPr is None:
            numPr = safe_get_prop(
                para_style.element,
                self._prop_path("numPr", f"{self._property_base}"),
            )
            if numPr is not None:
                return True
            base_style = self._styles.base_style(para_style)
            if not isinstance(base_style, para_style.__class__):
                return False
            para_style = base_style

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        para_style = self._styles.para_style(self._proxy.element)
        numPr: CT_NumPr | None = safe_get_prop(
            self._proxy, PropertyPath.base("numPr", "pPr")
        )
        if numPr is None and para_style is None:
            return self._from_0_numPr_0_para_style(property_path)
        elif numPr is None and para_style is not None:
            return self._from_0_numPr_1_para_style(property_path, para_style)
        elif numPr is not None and para_style is None:
            return self._from_1_numPr_0_para_style(property_path, numPr)
        elif numPr is not None and para_style is not None:
            # TODO: well, i will look for it in docs, temporary we prefer numbering over style
            val = self._from_1_numPr_0_para_style(
                property_path, numPr, para_style
            )
            if val is not None:
                return val
            return self._from_0_numPr_1_para_style(property_path, para_style)
        return None

    def _from_0_numPr_0_para_style(
        self, property_path: PropertyPath
    ) -> Any | None:
        doc_path = property_path.join_left("pPrDefault")
        if self._proxy.in_body:
            return self._from_doc_dflts(doc_path)
        tc_elm = cast("CT_Tc", self._proxy._parent.element)  # type: ignore
        table_val = self._from_table_style_hierarchy(tc_elm, property_path)
        if table_val is not None:
            return table_val
        return self._from_doc_dflts(doc_path)

    def _from_0_numPr_1_para_style(
        self, property_path: PropertyPath, para_style: ParagraphStyle
    ) -> Any | None:
        val = None
        numPr: CT_NumPr | None = None
        while val is None:
            numPr = safe_get_prop(
                para_style.element,
                self._prop_path("numPr", f"{self._property_base}"),
            )
            if numPr is not None:
                return self._from_1_numPr_0_para_style(
                    property_path, numPr, para_style
                )
            val = safe_get_prop(para_style.element, property_path)
            base_style = self._styles.base_style(para_style)
            if not isinstance(base_style, para_style.__class__):
                return val
            para_style = base_style
        return val

    def _from_1_numPr_0_para_style(
        self,
        property_path: PropertyPath,
        numPr: CT_NumPr,
        last_para_style: ParagraphStyle | None = None,
    ) -> Any | None:
        val = self._from_num_prop(property_path, numPr, last_para_style)
        if val is not None:
            return val
        return self._from_0_numPr_0_para_style(property_path)
