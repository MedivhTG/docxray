from typing import Any

# docxray stuff
from docxray.oxml.table.table import CT_Tc
from docxray.oxml.text.num_props import CT_NumPr
from docxray.oxml.text.paragraph import CT_P
from docxray.resolver.exceptions import ResolveError
from docxray.resolver.resolver import BaseResolver
from docxray.shared import PropertyPath, safe_get_prop
from docxray.styles.style import ParagraphStyle


class ParagraphResolver(BaseResolver[CT_P]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        para_style = self._styles.para_style(self._elm)
        numPr: CT_NumPr | None = safe_get_prop(
            self._elm, PropertyPath.base("numPr", "pPr")
        )
        if numPr is None and para_style is None:
            return self._from_0_numPr_0_para_style(property_path)
        elif numPr is None and para_style is not None:
            return self._from_0_numPr_1_para_style(property_path, para_style)
        elif numPr is not None and para_style is None:
            return self._from_1_numPr_0_para_style(property_path, numPr)
        elif numPr is not None and para_style is not None:
            msg = f"Сannot have list formatting and paragraph style at the same time for {self._elm}"
            raise ResolveError(msg)
        return None

    def _from_0_numPr_0_para_style(
        self, property_path: PropertyPath
    ) -> Any | None:
        tc_elm = self._elm.getparent(CT_Tc)
        if not isinstance(tc_elm, CT_Tc):
            return self._from_doc_dflts(property_path)
        table_val = self._from_table_style_hierarchy(tc_elm, property_path)
        if table_val is not None:
            return None
        return self._from_doc_dflts(property_path)

    def _from_0_numPr_1_para_style(
        self, property_path: PropertyPath, para_style: ParagraphStyle
    ) -> Any | None:
        val = None
        numPr: CT_NumPr | None = None
        while val is None:
            numPr = safe_get_prop(
                para_style.element,
                self._prop_val_path("numPr", f"{self._property_base}"),
            )
            if numPr is not None:
                return self._from_1_numPr_0_para_style(property_path, numPr)
            val = safe_get_prop(para_style.element, property_path)
            base_style = self._styles.base_style(para_style)
            if not isinstance(base_style, para_style.__class__):
                return val
            para_style = base_style
        return val

    def _from_1_numPr_0_para_style(
        self, property_path: PropertyPath, numPr: CT_NumPr
    ) -> Any | None:
        return None
