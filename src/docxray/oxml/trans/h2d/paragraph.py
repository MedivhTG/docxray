from functools import cached_property
from typing import Any

# docxray stuff
from docxray.exceptions import InvalidXmlError
from docxray.oxml.trans.proxy.numbering.numbering import (
    Level,
    LevelOverride,
    Num,
)
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
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
    def _associated_level(self) -> Level | LevelOverride | None:
        numPr_elm_direct = self._numPr_para_direct

        if numPr_elm_direct is None:
            numPr_elm_style = self._numPr_para_style
            if numPr_elm_style is not None:
                para_style_num_ref = self._para_style_num_ref
                # Never
                if para_style_num_ref is None:
                    return None

                return self._case_2_num_pr_style_ref(
                    numPr_elm_style, para_style_num_ref
                )
        else:
            return self._case_1_num_pr_direct(numPr_elm_direct)
        return None

    # TODO: if numId or ilvl omitted, then there is no numbering reference?
    def _case_1_num_pr_direct(
        self, numPr_elm: CT_NumPr
    ) -> Level | LevelOverride:
        numId_elm = numPr_elm.numId
        err = InvalidXmlError(f"Wrong numbering for {numPr_elm}")
        if numId_elm is None:
            raise err
        ilvl_elm = numPr_elm.ilvl
        if ilvl_elm is None:
            raise err
        if self._numbering is None:
            raise err
        num = self._find_real_num(numId_elm.val)
        lvl = num.associated_lvl_override(ilvl_elm.val)
        if lvl is not None:
            return lvl
        return num.abstract_num.lvl_by_ilvl(ilvl_elm.val)

    def _case_2_num_pr_style_ref(
        self, numPr_elm: CT_NumPr, para_style: ParagraphStyle
    ) -> Level:
        numId_elm = numPr_elm.numId
        err = InvalidXmlError(f"Wrong numbering for {numPr_elm}")
        if numId_elm is None:
            raise err
        if self._numbering is None:
            raise err
        num = self._find_real_num(numId_elm.val)
        style_id = para_style.element.name
        if style_id is None:
            raise err
        return num.abstract_num.lvl_by_para_style(style_id.val)

    def _find_real_num(self, num_id: int) -> Num:
        if self._numbering is None:
            raise InvalidXmlError(f"Wrong numbering for {num_id}")
        num = self._numbering.get_num(num_id)
        abstract_num = num.abstract_num
        num_style = abstract_num.numbering_style
        # Real abstract num can be hidden in deep inheritance
        while num_style:
            num = num_style.num
            abstract_num = num.abstract_num
            num_style = abstract_num.numbering_style
        return num

    @cached_property
    def _para_style_numbering(self) -> ParagraphStyle | None:
        level = self._associated_level
        if level is None:
            return None
        if isinstance(level, LevelOverride):
            if level.lvl is not None:
                return level.lvl.paragraph_style
        else:
            return level.paragraph_style
        return None

    @cached_property
    def _numPr_para_style(self) -> CT_NumPr | None:
        if self._para_style_num_ref is None:
            return None
        path = self._prop_path("numPr", self._path_base)
        numPr_elm = safe_get_prop(self._para_style_num_ref.element, path)
        if numPr_elm is None:
            return None
        return numPr_elm

    @cached_property
    def _numPr_para_direct(self) -> CT_NumPr | None:
        numPr_elm = self._prop("numPr")
        if isinstance(numPr_elm, NotFound):
            return None
        return numPr_elm

    @cached_property
    def _para_style_num_ref(self) -> ParagraphStyle | None:
        if self._para_style_direct is None:
            return None
        para_style: Any = self._para_style_direct
        path = self._prop_path("numPr", self._path_base)
        while isinstance(para_style, ParagraphStyle):
            numPr_elm = safe_get_prop(para_style.element, path)
            if not isinstance(numPr_elm, NotFound):
                return para_style
            para_style = para_style.base_style
        return None

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
        style_val = self._from_style_inheritance(
            self._para_style_direct, path, optional
        )
        if not isinstance(style_val, NotFound):
            return style_val
        if self._para_style_numbering is None:
            return style_val
        return self._from_style_inheritance(
            self._para_style_numbering, path, optional
        )
