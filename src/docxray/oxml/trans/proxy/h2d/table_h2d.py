from functools import cached_property
from typing import Literal

# docxray stuff
from docxray.oxml.trans.enums import (
    WD_CNF_FORMAT,
    WD_CNF_TABLE_LOOK,
    CnfLookName,
)
from docxray.oxml.trans.proxy.compute import width
from docxray.oxml.trans.proxy.shared import NotFound, Twips, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import TableStyle
from docxray.oxml.trans.st.enums import SE_Border
from docxray.oxml.trans.styles import CT_TblStylePr
from docxray.oxml.trans.table.table_props import CT_TblBorders

from .how_to_display import How2Display
from .table_rslv import CellResolver, RowResolver, TableResolver


class TableH2D(How2Display[TableResolver]):
    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        mask: bytes | None = self._rslvr.prop_val("tblLook", optional=True)
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)

    @cached_property
    def _tblBorders(self) -> CT_TblBorders | None:
        tblBorders_elm = self._rslvr.prop("tblBorders", algorithm="both")
        if isinstance(tblBorders_elm, NotFound):
            return None
        return tblBorders_elm


class RowH2D(How2Display[RowResolver]):
    @cached_property
    def first_row_show(self) -> bool:
        return self._format_from_cnf_look("firstRow")

    @cached_property
    def last_row_show(self) -> bool:
        return self._format_from_cnf_look("lastRow")

    @cached_property
    def first_col_show(self) -> bool:
        return self._format_from_cnf_look("firstColumn")

    @cached_property
    def last_col_show(self) -> bool:
        return self._format_from_cnf_look("lastColumn")

    @cached_property
    def no_horizontal_lines(self) -> bool:
        return self._format_from_cnf_look("noHBand")

    @cached_property
    def no_vertical_lines(self) -> bool:
        return self._format_from_cnf_look("noVBand")

    def _format_from_cnf_look(self, format_name: CnfLookName) -> bool:
        return self._cnf_look.has_format(format_name)

    @cached_property
    def _cnf(self) -> WD_CNF_FORMAT | None:
        cnf = self._rslvr.prop_val("cnfStyle")
        if isinstance(cnf, NotFound):
            return None
        return WD_CNF_FORMAT.from_string(cnf)

    @cached_property
    def _cnf_look(self) -> WD_CNF_TABLE_LOOK:
        if self._rslvr.tblPrEx is None:
            return self._rslvr.table.h2d._cnf_look
        mask: bytes | None = safe_get_prop(
            self._rslvr.tblPrEx, self._rslvr.prop_path("val", "tblLook")
        )
        if mask is None:
            return WD_CNF_TABLE_LOOK.from_bytes(b"")
        return WD_CNF_TABLE_LOOK.from_bytes(mask)

    @cached_property
    def _tblBorders(self) -> CT_TblBorders | None:
        if self._rslvr.tblPrEx is not None:
            return self._rslvr.tblPrEx.tblBorders
        return self._rslvr.table.h2d._tblBorders


type Border = Literal["top", "bottom", "left", "right"]


class CellH2D(How2Display[CellResolver]):
    # @cached_property
    # def top(self) -> SE_Border | None:
    #     spacing = self._rslvr.row.h2d._tblCellSpacing
    #     side = "top"
    #     if spacing is not None and spacing > 0:
    #         return self._side_cell_spacing(side)
    #     return self._side_no_cell_spacing(side)

    def _side_cell_spacing(self, side: str) -> None:
        pass

    def _side_no_cell_spacing(self, side: Border) -> None:
        pass

    def _side_val(self, side: str) -> SE_Border | None:
        path = self._rslvr.prop_path(
            "val", f"{self._rslvr._path_base}.tcBorders.{side}"
        )
        side_val = self._rslvr.from_tbl_style_hierarchy(
            self._has_cnf,
            self._tbl_style_props_deep,
            path,
        )
        if isinstance(side_val, NotFound) or side_val in (
            SE_Border.NULL,
            SE_Border.NONE,
        ):
            return None
        return side_val

    # TODO: realize as:
    # remark) `insideH`/`insideV` about lines inside
    # grid group with horizontal/vertical borders
    # without (topmost, botmost)/(leftmost, rightmost) borders rendered -
    # they are rendered by `top`/`bottom`/`left`/`right` sides instead.
    #
    # 1) Modify `from_tbl_style_hierarchy` method to return
    # context where property got in tuple (prop and context).
    #
    # 2) If property got in table style direct level or
    # from row-level `tblBorders` or `tblBorders` then
    # cell in group of `wholeTable`
    #
    # 3) Split logic as follows:
    #
    # 3.1) If context is `wholeTable` then pos of cell
    # derived like in table grid (look point `remark`)
    #
    # 3.2) If context is `firsRow`/`lastRow`/`band1Horz`/`band2Horz`
    # then pos of cell derived as
    # in single row (cells above and below are not exist) and
    # `insideH` has no meaning in context.
    #
    # 3.3) If context is `firstCol`/`lastCol`/`band1Vert`/`band2Vert`
    # then pos of cell derived as
    # in single column (cells prev and next are not exist) and
    # `insideV` has no meaning in context.
    #
    # 3.4) If context is `nwCell`/`neCell`/`swCell`/`seCell`
    # then pos of cell derived as single cell (no adjacent cells) and
    # `insideV` with `insideH` has no meaning in context.
    #
    # 4) If sides as `insideH` or `insideV` has meaning in context
    # of cell groups but ommited in all levels then get their
    # fallback analogs (for 1st - top/bottom, for 2nd - left/right).
    #

    @cached_property
    def _side_context(self) -> None:
        pass

    @cached_property
    def _tblCellSpacing(self) -> Twips | float | None:
        name = "tblCellSpacing"
        row_rslvr = self._rslvr.row_resolver
        tbl_rslvr = row_rslvr.table_resolver
        # Row-level direct
        spacing_elm = row_rslvr.prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm)
        # Row-level exception
        tblPrEx_elm = row_rslvr.tblPrEx
        if tblPrEx_elm is not None:
            spacing_elm = tblPrEx_elm.tblCellSpacing
            if spacing_elm is not None:
                return width(spacing_elm)
        # Table-level
        spacing_elm = tbl_rslvr.prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm)

        # From table style (defined common or exception)
        path = row_rslvr.prop_path(name, row_rslvr._path_base)
        # Table style Row-level (in grid group or direct) firstly
        spacing_elm = self._rslvr.from_tbl_style_hierarchy(
            self._has_cnf, self._tbl_style_props_deep, path
        )
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm)
        # Table style Table-level (in grid group or direct) lastly
        path = tbl_rslvr.prop_path(name, tbl_rslvr._path_base)
        spacing_elm = self._rslvr.from_tbl_style_hierarchy(
            self._has_cnf, self._tbl_style_props_deep, path
        )
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm)
        return None

    @cached_property
    def _cnf(self) -> WD_CNF_FORMAT | None:
        cnf = self._rslvr.prop_val("cnfStyle")
        if isinstance(cnf, NotFound):
            return None
        return WD_CNF_FORMAT.from_string(cnf)

    @cached_property
    def _cnf_row(self) -> WD_CNF_FORMAT | None:
        return self._rslvr.row.h2d._cnf

    @cached_property
    def _cnf_gathered(self) -> WD_CNF_FORMAT | None:
        cnf_cell = self._cnf
        cnf_row = self._cnf_row
        cnf = cnf_cell
        if cnf_row is not None:
            if cnf is None:
                cnf = cnf_row
            else:
                cnf |= cnf_row
        if cnf is None:
            return None
        return self._cnf_looked(cnf)

    @cached_property
    def _has_cnf(self) -> bool:
        return False if self._cnf_gathered is None else True

    @cached_property
    def _tbl_style_props_deep(
        self,
    ) -> list[tuple[TableStyle, list[CT_TblStylePr]]]:
        tbl_style = self._rslvr.table_style
        props_leveled = []
        cnf = self._cnf_gathered
        while isinstance(tbl_style, TableStyle):
            if cnf is not None:
                tbl_style_props = self._rslvr.table_style_props(tbl_style, cnf)
            else:
                tbl_style_props = []
            props_leveled.append((tbl_style, tbl_style_props))
            tbl_style = self._rslvr._styles.base_style(tbl_style)  # type: ignore[assignment]
        return props_leveled

    def _cnf_looked(self, cnf: WD_CNF_FORMAT) -> WD_CNF_FORMAT:
        row_h2d = self._rslvr.row.h2d
        if not row_h2d.first_row_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
        if not row_h2d.last_row_show:
            cnf &= ~WD_CNF_FORMAT.LAST_ROW
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if not row_h2d.first_col_show:
            cnf &= ~WD_CNF_FORMAT.FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN
        if not row_h2d.last_col_show:
            cnf &= ~WD_CNF_FORMAT.LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN
            cnf &= ~WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN
        if row_h2d.no_horizontal_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_HORIZONTAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND
        if row_h2d.no_vertical_lines:
            cnf &= ~WD_CNF_FORMAT.ODD_VERTICAL_BAND
            cnf &= ~WD_CNF_FORMAT.EVEN_VERTICAL_BAND
        return cnf
