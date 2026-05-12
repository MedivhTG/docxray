from functools import cached_property
from typing import Literal

# docxray stuff
from docxray.enum.lxml import POS
from docxray.oxml.trans.enums import (
    WD_CNF_FORMAT,
    WD_CNF_TABLE_LOOK,
    CnfLookName,
)
from docxray.oxml.trans.proxy.compute import width
from docxray.oxml.trans.proxy.shared import NotFound, Twips, safe_get_prop
from docxray.oxml.trans.proxy.styles.style import TableStyle
from docxray.oxml.trans.st.enums import SE_Border, SE_TblStyleOverrideType
from docxray.oxml.trans.styles import CT_TblStylePr
from docxray.oxml.trans.table.cell_props import CT_TcBorders
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


type _Border = Literal["top", "bottom", "left", "right", "insideH", "insideV"]
type _TableChild = Literal["row", "cell"]

TBL_POSITIONING: dict[POS, dict[_TableChild, tuple[_Border, _Border]]] = {
    POS.ONE_ITEM: {
        "row": ("top", "bottom"),
        "cell": ("left", "right"),
    },
    POS.START: {
        "row": ("top", "insideH"),
        "cell": ("left", "insideV"),
    },
    POS.MIDDLE: {
        "row": ("insideH", "insideH"),
        "cell": ("insideV", "insideV"),
    },
    POS.END: {
        "row": ("insideH", "bottom"),
        "cell": ("insideV", "right"),
    },
}


class CellH2D(How2Display[CellResolver]):
    @cached_property
    def borders_info(self) -> dict:
        """Get info about cell borders.

        Returns:
            dict: _description_
        """
        spacing = self._tblCellSpacing
        if spacing is not None and spacing > 0:
            return self._spacing_non_zero()
        return self._spacing_non_zero()

    def _spacing_non_zero(self) -> dict:
        tcBorders_elm, cell_ctx = self._cell_borders_ctx
        tblBorders_elm = self._rslvr.row.h2d._tblBorders
        tbl_horz = self._border(tblBorders_elm, "insideH")
        tbl_vert = self._border(tblBorders_elm, "insideV")
        if tcBorders_elm is None and cell_ctx is None:
            return self._case_1_tc_borders_ommited(tbl_horz, tbl_vert)
        if tcBorders_elm is not None and cell_ctx is None:
            return self._case_2_tc_borders_direct(
                tcBorders_elm, tbl_horz, tbl_vert
            )
        if tcBorders_elm is not None and isinstance(cell_ctx, TableStyle):
            return self._case_3_tc_borders_style_direct(
                tcBorders_elm, tbl_horz, tbl_vert
            )
        if tcBorders_elm is not None and isinstance(cell_ctx, CT_TblStylePr):
            return self._case_4_tc_borders_grid_group(
                tcBorders_elm, tbl_horz, tbl_vert, cell_ctx.type
            )
        # TODO: Refac
        raise Exception("Reached Never")

    def _case_1_tc_borders_ommited(
        self, tbl_horz: SE_Border | None, tbl_vert: SE_Border | None
    ) -> dict:
        return {
            "top": tbl_horz,
            "bottom": tbl_horz,
            "left": tbl_vert,
            "right": tbl_vert,
        }

    def _case_2_tc_borders_direct(
        self,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: SE_Border | None,
        tbl_vert: SE_Border | None,
    ) -> dict:
        return {
            "top": self._border(tcBorders_elm, "top") or tbl_horz,
            "bottom": self._border(tcBorders_elm, "bottom") or tbl_horz,
            "left": self._border(tcBorders_elm, "left") or tbl_vert,
            "right": self._border(tcBorders_elm, "right") or tbl_vert,
        }

    def _case_3_tc_borders_style_direct(
        self,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: SE_Border | None,
        tbl_vert: SE_Border | None,
    ) -> dict:
        return self._case_2_tc_borders_direct(
            tcBorders_elm, tbl_horz, tbl_vert
        )

    # TODO: refac if needed
    def _case_4_tc_borders_grid_group(
        self,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: SE_Border | None,
        tbl_vert: SE_Border | None,
        grid_group: SE_TblStyleOverrideType,
    ) -> dict[str, SE_Border | None]:
        G = SE_TblStyleOverrideType
        cell = self._rslvr._proxy
        row = cell.row
        top = None
        bottom = None
        left = None
        right = None
        if grid_group == G.ENTIRE_TABLE:
            top, bottom = self._choose_horz(row.pos, tcBorders_elm, tbl_horz)
            left, right = self._choose_vert(cell.pos, tcBorders_elm, tbl_vert)
        elif grid_group in (
            G.HEADER_ROW,
            G.FOOTER_ROW,
            G.HORIZONTAL_BAND_ODD,
            G.HORIZONTAL_BAND_EVEN,
        ):
            top, bottom = self._choose_horz(
                POS.ONE_ITEM, tcBorders_elm, tbl_horz
            )
            left, right = self._choose_vert(cell.pos, tcBorders_elm, tbl_vert)
        elif grid_group in (
            G.FIRST_COLUMN,
            G.LAST_COLUMN,
            G.VERTICAL_BAND_ODD,
            G.VERTICAL_BAND_EVEN,
        ):
            top, bottom = self._choose_horz(row.pos, tcBorders_elm, tbl_horz)
            left, right = self._choose_vert(
                POS.ONE_ITEM, tcBorders_elm, tbl_vert
            )
        elif grid_group in (
            G.TOP_LEFT_CORNER_CELL,
            G.TOP_RIGHT_CORNER_CELL,
            G.BOTTOM_LEFT_CORNER_CELL,
            G.BOTTOM_RIGHT_CORNER_CELL,
        ):
            top, bottom = self._choose_horz(
                POS.ONE_ITEM, tcBorders_elm, tbl_horz
            )
            left, right = self._choose_vert(
                POS.ONE_ITEM, tcBorders_elm, tbl_vert
            )
        return {"top": top, "bottom": bottom, "left": left, "right": right}

    def _choose_horz(
        self,
        row_pos: POS,
        tcBorders_elm: CT_TcBorders,
        tbl_horz: SE_Border | None,
    ) -> tuple[SE_Border | None, SE_Border | None]:
        top_n, bottom_n = TBL_POSITIONING[row_pos]["row"]
        top = self._border(tcBorders_elm, top_n)
        if top_n == "insideH" and top is None:
            top = self._border(tcBorders_elm, "top") or tbl_horz
        bottom = self._border(tcBorders_elm, bottom_n)
        if bottom_n == "insideH" and bottom is None:
            bottom = self._border(tcBorders_elm, "bottom") or tbl_horz
        return top, bottom

    def _choose_vert(
        self,
        cell_pos: POS,
        tcBorders_elm: CT_TcBorders,
        tbl_vert: SE_Border | None,
    ) -> tuple[SE_Border | None, SE_Border | None]:
        left_n, right_n = TBL_POSITIONING[cell_pos]["cell"]
        left = self._border(tcBorders_elm, left_n)
        if left_n == "insideV" and left is None:
            left = self._border(tcBorders_elm, "left") or tbl_vert
        right = self._border(tcBorders_elm, right_n)
        if right_n == "insideV" and right is None:
            right = self._border(tcBorders_elm, "right") or tbl_vert
        return left, right

    def _border(
        self, borders_elm: CT_TcBorders | CT_TblBorders | None, border: _Border
    ) -> SE_Border | None:
        path = self._rslvr.prop_path("val", border)
        prop = safe_get_prop(borders_elm, path)
        if isinstance(prop, NotFound):
            return None
        return prop

    # TODO: realize and use in `borders_info`
    def _spacing_zero(self) -> dict:
        raise NotImplementedError()

    @cached_property
    def _cell_borders_ctx(
        self,
    ) -> tuple[CT_TcBorders | None, TableStyle | CT_TblStylePr | None]:
        name = "tcBorders"
        # Direct
        tcBorders_elm = self._rslvr.prop(name)
        if not isinstance(tcBorders_elm, NotFound):
            return tcBorders_elm, None
        # From table style (defined common or exception)
        # whenever in grid group or directly
        path = self._rslvr.prop_path(name, self._rslvr._path_base)
        tc_ctx = self._rslvr.from_tbl_style_hierarchy(
            self._has_cnf, self._tbl_style_props_deep, path
        )
        if not isinstance(tc_ctx[0], NotFound):
            return tc_ctx
        return None, None

    @cached_property
    def _tblCellSpacing(self) -> Twips | float | None:
        """Get spacing between cells for current depending on the cell context.

        Returns:
            Twips | float | None: Measure in `Twips` or set to `None`. `float`
                type (percents) impossible but written for typing compat.
        """
        name = "tblCellSpacing"
        row_rslvr = self._rslvr.row_resolver
        tbl_rslvr = row_rslvr.table_resolver
        # Row-level direct
        spacing_elm = row_rslvr.prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        # Row-level exception
        tblPrEx_elm = row_rslvr.tblPrEx
        if tblPrEx_elm is not None:
            spacing_elm = tblPrEx_elm.tblCellSpacing
            if spacing_elm is not None:
                return width(spacing_elm, True)
        # Table-level
        spacing_elm = tbl_rslvr.prop(name)
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)

        # From table style (defined common or exception)
        path = row_rslvr.prop_path(name, row_rslvr._path_base)
        # Table style Row-level (in grid group or direct) firstly
        spacing_elm, _ = self._rslvr.from_tbl_style_hierarchy(
            self._has_cnf, self._tbl_style_props_deep, path
        )
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
        # Table style Table-level (in grid group or direct) lastly
        path = tbl_rslvr.prop_path(name, tbl_rslvr._path_base)
        spacing_elm, _ = self._rslvr.from_tbl_style_hierarchy(
            self._has_cnf, self._tbl_style_props_deep, path
        )
        if not isinstance(spacing_elm, NotFound):
            return width(spacing_elm, True)
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
