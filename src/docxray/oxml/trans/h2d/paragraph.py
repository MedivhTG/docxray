from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.shared import NotFound, PropertyPath
from docxray.oxml.trans.proxy.styles.style import (
    S_TYPE_TO_STYLE_CLS,
    ParagraphStyle,
)
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.st.enums import SE_StyleType
from docxray.oxml.trans.text.num_props import CT_NumPr

from .how2display import How2Display


class ParagraphH2D(How2Display[Paragraph]):
    @cached_property
    def cell(self) -> Cell | None:
        container = self._proxy.container
        if isinstance(container, Cell):
            return container
        return None

    @cached_property
    def _para_style_numbering(self) -> ParagraphStyle | None:
        return None

    @cached_property
    def _foo(self):
        numPr_elm = self._numPr_para_direct
        if numPr_elm is not None:
            return self._case_1_num_pr_direct(numPr_elm)

    # TODO: if numId or ilvl omitted, then there is no numbering reference?
    def _case_1_num_pr_direct(self, numPr_elm: CT_NumPr):
        numId_elm = numPr_elm.numId
        if numId_elm is None:
            return None
        ilvl_elm = numPr_elm.ilvl
        if ilvl_elm is None:
            return None
        if self._numbering is None:
            return None
        return self._numbering.associated_lvl(numId_elm.val, ilvl_elm.val)

    @cached_property
    def _numPr_para_para_style(self) -> CT_NumPr | None:
        numPr_elm = self._prop("numPr", algorithm="style")
        if isinstance(numPr_elm, NotFound):
            return None
        return numPr_elm

    @cached_property
    def _numPr_para_direct(self) -> CT_NumPr | None:
        numPr_elm = self._prop("numPr")
        if isinstance(numPr_elm, NotFound):
            return None
        return numPr_elm

    @cached_property
    def _para_style_direct(self) -> ParagraphStyle | None:
        style_id = self._prop_val("pStyle")
        if isinstance(style_id, NotFound):
            return None
        return self._styles.get_by_id(
            style_id,
            SE_StyleType.PARAGRAPH,
            S_TYPE_TO_STYLE_CLS[SE_StyleType.PARAGRAPH],
        )

    def _prop_val_run(self, name: str, optional: bool = True) -> Any:
        path = self._prop_path("val", f"rPr.{name}")
        return self._from_styles_hierarchy(path, optional)

    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        if self._para_style_direct is None:
            return NotFound(self, path)
        return self._from_style_inheritance(
            self._para_style_direct, path, optional
        )
