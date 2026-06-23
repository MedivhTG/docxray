from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.h2d.border import Border
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.st.enums import (
    SE_BORDER,
    SE_JC_TABLE,
    SE_TBL_LAYOUT_TYPE,
    SE_VERTICAL_JC,
)

from .base import HtmlBuilder
from .std import TEXT_FLOW_TO_WRITING_MODE, pt

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.table import Cell, Row, Table
    from docxray.transform.ruleset import RuleSet


class HtmlTable(HtmlBuilder["Table"]):
    VALIGN_TO_HTML_VALGN = {
        SE_VERTICAL_JC.TOP: "top",
        SE_VERTICAL_JC.CENTER: "middle",
        SE_VERTICAL_JC.BOTTOM: "bottom",
        SE_VERTICAL_JC.BOTH: "middle",
    }
    SE_BORDER_TO_CSS = {
        SE_BORDER.SINGLE: (1, "solid"),
        SE_BORDER.THICK: (5, "solid"),
        SE_BORDER.DOUBLE: (3, "double"),
        SE_BORDER.DOTTED: (2, "dotted"),
        SE_BORDER.DASHED: (2, "dashed"),
        SE_BORDER.DOT_DASH: (2, "dashed"),
        SE_BORDER.DOT_DOT_DASH: (2, "dashed"),
        SE_BORDER.TRIPLE: (2, "double"),
        SE_BORDER.THIN_THICK_SMALL_GAP: (5, "solid"),
        SE_BORDER.THICK_THIN_SMALL_GAP: (5, "solid"),
        SE_BORDER.THIN_THICK_THIN_SMALL_GAP: (5, "solid"),
        SE_BORDER.THIN_THICK_MEDIUM_GAP: (3, "double"),
        SE_BORDER.THICK_THIN_MEDIUM_GAP: (3, "double"),
        SE_BORDER.THIN_THICK_THIN_MEDIUM_GAP: (3, "double"),
        SE_BORDER.THIN_THICK_LARGE_GAP: (4, "double"),
        SE_BORDER.THICK_THIN_LARGE_GAP: (4, "double"),
        SE_BORDER.THIN_THICK_THIN_LARGE_GAP: (4, "double"),
        SE_BORDER.WAVE: (3, "groove"),
        SE_BORDER.DOUBLE_WAVE: (3, "ridge"),
        SE_BORDER.DASH_SMALL_GAP: (2, "dashed"),
        SE_BORDER.DASH_DOT_STROKED: (2, "dotted"),
        SE_BORDER.THREE_D_EMBOSS: (3, "ridge"),
        SE_BORDER.THREE_D_ENGRAVE: (3, "groove"),
        SE_BORDER.OUTSET: (3, "outset"),
        SE_BORDER.INSET: (3, "inset"),
    }

    @classmethod
    def element(cls, proxy: Table, ruleset: RuleSet) -> HtmlElement:
        return cls._table(proxy, ruleset)

    @classmethod
    def _table(cls, proxy: Table, ruleset: RuleSet) -> HtmlElement:
        table_elm = Element("table", cls._table_attrs(proxy))
        for row in proxy.iter_rows():
            table_elm.append(cls._row(row, ruleset))
        return table_elm

    @classmethod
    def _row(cls, proxy: Row, ruleset: RuleSet) -> HtmlElement:
        tr_elm = Element("tr", cls._row_attrs(proxy))
        for cell in proxy.iter_cells():
            tr_elm.append(cls._cell(cell, ruleset))
        return tr_elm

    @classmethod
    def _row_attrs(cls, proxy: Row) -> dict[str, str]:
        attrs: dict[str, str] = {}
        if proxy.height is not None:
            attrs["height"] = f"{proxy.height.pt}pt"
        return attrs

    @classmethod
    def _cell(cls, proxy: Cell, ruleset: RuleSet) -> HtmlElement:
        td_elm = Element("td", cls._cell_attrs(proxy))
        transform_lists = ruleset.html_rules["Table"].opts.get(
            "transform_list_views"
        )
        if transform_lists:
            for item in proxy.iter_inner_content_with_lists():
                item_elm = item.transform(ruleset, stringify=False)
                td_elm.append(item_elm)
        else:
            for item in proxy.iter_inner_content():
                item_elm = item.transform(ruleset, stringify=False)
                td_elm.append(item_elm)
        return td_elm

    @classmethod
    def _cell_attrs(cls, proxy: Cell) -> dict[str, str]:
        attrs: dict[str, str] = {}
        if proxy.width is not None:
            attrs["width"] = pt(proxy.width)
        if proxy.vert_span and proxy.vert_span > 1:
            attrs["rowspan"] = str(proxy.vert_span)
        if proxy.horz_span > 1:
            attrs["colspan"] = str(proxy.horz_span)
        style = cls._cell_style(proxy)
        if style:
            attrs["style"] = style
        return attrs

    @classmethod
    def _cell_style(cls, proxy: Cell) -> str:
        style = ""
        sides: list[str] = ["top", "bottom", "left", "right"]
        for side in sides:
            border: str = cls._cell_border(proxy.borders_info[side], side)  # type: ignore[literal-required]
            if border:
                style += border
        if proxy.content_flow is not None:
            style += f"writing-mode: {TEXT_FLOW_TO_WRITING_MODE[proxy.content_flow]}; "
        if proxy.vertical_alignment:
            valign = cls.VALIGN_TO_HTML_VALGN[proxy.vertical_alignment]
            style += f"vertical-align: {valign}; "
        padding = cls._cell_padding(proxy)
        if padding:
            style += padding
        return style

    @classmethod
    def _cell_border(cls, border: Border | None, side: str) -> str:
        border_side = ""

        if border is not None and border.border_type not in (
            SE_BORDER.NULL,
            SE_BORDER.NONE,
        ):
            dflt_size, line_type = cls.SE_BORDER_TO_CSS.get(
                border.border_type, (1, "solid")
            )
            given_size = -1 if border.size is None else border.size.px()
            size = f"{dflt_size if given_size < dflt_size else given_size}px"
            color = border.final_color or "black"
            border_side = f"border-{side}: {size} {line_type} {color}; "
        return border_side

    @classmethod
    def _cell_padding(cls, proxy: Cell) -> str:
        info = proxy.padding_info
        padding = ""
        sides = ["top", "bottom", "left", "right"]
        for side in sides:
            padding_side = info[side]  # type: ignore[literal-required]
            if padding_side is not None:
                padding += f"padding-{side}: {pt(padding_side)}; "
        return padding

    @classmethod
    def _table_attrs(cls, proxy: Table) -> dict[str, str]:
        attrs = {}
        if proxy.width is not None:
            attrs["width"] = pt(proxy.width)
        style = cls._table_style(proxy)
        if style:
            attrs["style"] = style
        return attrs

    @classmethod
    def _table_style(cls, proxy: Table) -> str:
        style = ""
        if proxy.spacing_first is None:
            style += "border-collapse: collapse; "
        else:
            spacing = proxy.spacing_first
            style += f"border-spacing: {pt(spacing)}; "
        if proxy.left_indent:
            style += f"margin-inline-start: {pt(proxy.left_indent)}; "
        if proxy.layout == SE_TBL_LAYOUT_TYPE.FIXED:
            style += "table-layout: fixed; "
        style += cls._table_alignment(proxy)
        return style

    @classmethod
    def _table_alignment(cls, proxy: Table) -> str:
        align = ""
        if proxy.alignment in {SE_JC_TABLE.LEFT, SE_JC_TABLE.START}:
            align += "margin-right: auto; "
        elif proxy.alignment in {SE_JC_TABLE.START, SE_JC_TABLE.END}:
            align += "margin-left: auto; "
        else:
            align += "margin-left: auto; margin-right: auto;"
        return align
