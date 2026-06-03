from __future__ import annotations

from abc import abstractmethod
from base64 import b64encode
from collections.abc import Callable
from copy import copy
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.h2d.border import Border
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.proxy.text.run import Run, Tab, TxtFragment
from docxray.oxml.trans.st.enums import (
    SE_JC,
    SE_LEVEL_SUFFIX,
    SE_LINE_SPACING_RULE,
    SE_TEXT_DIRECTION,
    SE_UNDERLINE,
    SE_VERTICAL_JC,
    SE_BORDER,
    SE_VerticalAlignRun,
)

from .utils.char_graph import RunChain, RunChainsMap

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.list_view import (
        ListViewIlvlBlock,
        ListViewInterrupted,
    )
    from docxray.oxml.trans.proxy.table import Cell, Row, Table
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph

    from .ruleset import RuleSet

T = TypeVar("T")

type ElmMaker = Callable[[Any], HtmlElement]
TAB_MNEMONIC = "&emsp;"
SPACEBREAK_MNEMONIC = "&nbsp;"
U_DECOR_MAP = {
    SE_UNDERLINE.SINGLE: "underline",
    SE_UNDERLINE.DOUBLE: "underline double",
    SE_UNDERLINE.DOTTED: "underline dotted",
    SE_UNDERLINE.DASH: "underline dashed",
    SE_UNDERLINE.WAVE: "underline wavy",
    SE_UNDERLINE.DOTTED_HEAVY: "underline dotted",
    SE_UNDERLINE.DASHED_HEAVY: "underline dashed",
    SE_UNDERLINE.DASH_LONG: "underline dashed",
    SE_UNDERLINE.DASH_LONG_HEAVY: "underline dashed",
    SE_UNDERLINE.DOT_DASH: "underline dotted",
    SE_UNDERLINE.DASH_DOT_HEAVY: "underline dashed",
    SE_UNDERLINE.DOT_DOT_DASH: "underline dotted",
    SE_UNDERLINE.DASH_DOT_DOT_HEAVY: "underline dashed",
    SE_UNDERLINE.WAVY_HEAVY: "underline wavy",
    SE_UNDERLINE.WAVY_DOUBLE: "underline waby",
}
TEXT_FLOW_TO_WRITING_MODE = {
    SE_TEXT_DIRECTION.TOP_TO_BOTTOM: "vertical-lr",
    SE_TEXT_DIRECTION.RIGHT_TO_LEFT: "horizontal-tb",
    SE_TEXT_DIRECTION.LEFT_TO_RIGHT: "horizontal-tb",
    SE_TEXT_DIRECTION.TOP_TO_BOTTOM_VERTICAL: "sideways-lr",
    SE_TEXT_DIRECTION.RIGHT_TO_LEFT_VERTICAL: "sideways-rl",
    SE_TEXT_DIRECTION.LEFT_TO_RIGHT_VERTICAL: "sideways-lr",
    SE_TEXT_DIRECTION.BOTTOM_TO_TOP_LEFT_TO_RIGHT: "horizontal-bt",
    SE_TEXT_DIRECTION.LEFT_TO_RIGHT_TOP_TO_BOTTOM: "horizontal-tb",
    SE_TEXT_DIRECTION.LEFT_TO_RIGHT_TOP_TO_BOTTOM_VERTICAL: "sideways-lr",
    SE_TEXT_DIRECTION.TOP_TO_BOTTOM_RIGHT_TO_LEFT: "vertical-rl",
    SE_TEXT_DIRECTION.TOP_TO_BOTTOM_RIGHT_TO_LEFT_VERTICAL: "sideways-rl",
}


class HtmlBuilder(Generic[T]):
    @classmethod
    @abstractmethod
    def element(cls, proxy: T, ruleset: RuleSet) -> HtmlElement: ...


def i_elm(value: bool) -> HtmlElement:
    return Element("i")


def b_elm(value: bool) -> HtmlElement:
    return Element("b")


def strike_elm(value: bool) -> HtmlElement:
    return Element("s")


def underline_elm(value: SE_UNDERLINE) -> HtmlElement:
    decor = U_DECOR_MAP.get(value)
    if decor is None:
        decor = "underline"
    return Element("span", {"style": f"text-decoration: {decor};"})


def vert_align_elm(value: SE_VerticalAlignRun) -> HtmlElement:
    if value == SE_VerticalAlignRun.SUPERSCRIPT:
        return Element("sup")
    return Element("sub")


def units(length: Length | float | None) -> str:
    if length is None:
        return ""
    elif isinstance(length, Length):
        return f"{length.pt}pt"
    else:
        return f"{length}%"


def tag_tree(
    run_proxy: Any,
    attr_to_elmmaker: dict[str, ElmMaker],
) -> tuple[HtmlElement, HtmlElement] | None:
    top = None
    bottom = None
    for attr, maker in attr_to_elmmaker.items():
        val = getattr(run_proxy, attr, None)
        if not val:
            continue
        elm = maker(val)
        if top is None and bottom is None:
            top = elm
            bottom = elm
        elif top is not None and bottom is not None:
            bottom.append(elm)
            bottom = elm
    if top is None or bottom is None:
        return None
    return top, bottom


class HtmlParagraph(HtmlBuilder["Paragraph"]):
    HL_TO_P_TAG = {
        WD_HEADER_LEVEL.TEXT: "p",
        WD_HEADER_LEVEL.HEADER_1: "h1",
        WD_HEADER_LEVEL.HEADER_2: "h2",
        WD_HEADER_LEVEL.HEADER_3: "h3",
        WD_HEADER_LEVEL.HEADER_4: "h4",
        WD_HEADER_LEVEL.HEADER_5: "h5",
        WD_HEADER_LEVEL.HEADER_6: "h6",
        WD_HEADER_LEVEL.HEADER_7: "h6",
        WD_HEADER_LEVEL.HEADER_8: "h6",
        WD_HEADER_LEVEL.HEADER_9: "h6",
    }
    ALGN_TO_ALGN = {
        SE_JC.START: "left",
        SE_JC.CENTER: "center",
        SE_JC.END: "right",
        SE_JC.BOTH: "justify",
        SE_JC.LEFT: "left",
        SE_JC.RIGHT: "right",
        SE_JC.NUM_TAB: "left",
    }
    ALGN_JSTFIED = {SE_JC.DISTRIBUTE, SE_JC.THAI_DISTRIBUTE}
    ALGN_TO_JSTFY = {
        SE_JC.MEDIUM_KASHIDA: "kashida",
        SE_JC.DISTRIBUTE: "distribute",
        SE_JC.HIGH_KASHIDA: "kashida",
        SE_JC.LOW_KASHIDA: "kashida",
        SE_JC.THAI_DISTRIBUTE: "distribute",
    }

    ATTR_TO_ELMMAKER: dict[str, ElmMaker] = {
        "underline": underline_elm,
        "vertical_alignment": vert_align_elm,
        "italic": i_elm,
        "bold": b_elm,
        "strike": strike_elm,
    }

    @classmethod
    def element(cls, proxy: Paragraph, ruleset: RuleSet) -> HtmlElement:
        elm = Element(cls.HL_TO_P_TAG[proxy.header_level], cls._attrs(proxy))
        list_item_content = cls._list_item_content(proxy)
        if isinstance(list_item_content, str):
            elm.text = list_item_content
        else:
            elm.append(list_item_content)
        cls._fill_content(proxy, elm, ruleset)
        return elm

    @classmethod
    def _fill_content(
        cls, proxy: Paragraph, elm: HtmlElement, ruleset: RuleSet
    ) -> None:
        if not proxy.has_text and not proxy.has_picture:
            elm.text = SPACEBREAK_MNEMONIC
            return
        chain_map = RunChainsMap(set(cls.ATTR_TO_ELMMAKER))
        for run_or_hlink in proxy.iter_inner_content():
            if isinstance(run_or_hlink, Run):
                chain_map.chain(run_or_hlink)
            else:
                for run in run_or_hlink.iter_inner_content():
                    chain_map.chain(run)
        runs_builder = _RunsHtmlBuilder(elm, cls.ATTR_TO_ELMMAKER, ruleset)
        for unchained_or_chain in chain_map.chains_ordered():
            if isinstance(unchained_or_chain, Run):
                runs_builder.run(elm, unchained_or_chain)
            else:
                runs_builder.run_chain(unchained_or_chain)

    @classmethod
    def _list_item_content(cls, proxy: Paragraph) -> str | HtmlElement:
        if proxy.list_item is None:
            return ""
        li = proxy.list_item
        txt = li.level_text
        if li.chars_case == "up":
            txt = txt.upper()
        elif li.chars_case == "down":
            txt = txt.lower()
        tree = tag_tree(li, cls.ATTR_TO_ELMMAKER)
        suff = li.level.separator
        if suff == SE_LEVEL_SUFFIX.TAB:
            sep = TAB_MNEMONIC
        elif suff == SE_LEVEL_SUFFIX.SPACE:
            sep = " "
        else:
            sep = ""
        if tree is None:
            return txt + sep
        top, bottom = tree
        bottom.text = txt
        top.tail = sep
        return top

    @classmethod
    def _attrs(cls, proxy: Paragraph) -> dict[str, str]:
        attrs = {}
        if proxy.right_to_left:
            attrs["dir"] = "rtl"
        style = cls._style(proxy)
        if style:
            attrs["style"] = style
        return attrs

    @classmethod
    def _style(cls, proxy: Paragraph) -> str:
        style = ""
        if proxy.margin_line_start:
            style += (
                f"margin-inline-start: {cls._ind(proxy.margin_line_start)}; "
            )
        if proxy.margin_line_end:
            style += f"margin-inline-end: {cls._ind(proxy.margin_line_end)}; "
        if proxy.text_indent:
            style += f"text-indent: {cls._ind(proxy.text_indent)}; "
        style += cls._alignment(proxy)
        if proxy.text_flow is not None:
            style += (
                f"writing-mode: {TEXT_FLOW_TO_WRITING_MODE[proxy.text_flow]}; "
            )
        h2d = proxy.h2d
        if h2d.keep_next:
            style += "page-break-after: avoid; "
        if h2d.keep_lines:
            style += "page-break-inside: avoid; "
        if h2d.page_break_before:
            style += "page-break-before: always;"
        if h2d.no_hanging and not h2d.keep_lines:
            style += "page-break-inside: avoid; orphans: 2; widows: 2; "
        else:
            style += "orphans: 2; widows: 2; "
        if not h2d.word_wrap:
            style += "word-break: break-all; "
        if h2d.supress_auto_hyphens:
            style += "hyphens: manual; "
        spacing = cls._spacing(proxy)
        if spacing:
            style += spacing
        return style

    @classmethod
    def _spacing(cls, proxy: Paragraph) -> str:
        spacing = ""
        if proxy.margin_top is not None:
            spacing += f"margin-top: {cls._margin(proxy.margin_top)}; "
        else:
            spacing += "margin-top: 0pt; "
        if proxy.margin_bottom is not None:
            spacing += f"margin-bottom: {cls._margin(proxy.margin_bottom)}; "
        else:
            spacing += "margin-bottom: 0pt; "
        if proxy.line_height is not None:
            units = ""
            if proxy.line_rule == SE_LINE_SPACING_RULE.AUTO:
                if not isinstance(proxy.line_height, Length):
                    result = proxy.line_height / 240
                    units = f"{result:.2f}"
            else:
                if isinstance(proxy.line_height, Length):
                    units = f"{proxy.line_height.pt}pt"
            if units:
                spacing += f"line-height: {units}; "
        return spacing

    @classmethod
    def _alignment(cls, proxy: Paragraph) -> str:
        alignment = proxy.alignment
        algn = ""
        if alignment in cls.ALGN_TO_ALGN:
            if proxy.right_to_left and alignment in (SE_JC.START, SE_JC.LEFT):
                algn += f"text-align: {cls.ALGN_TO_ALGN[SE_JC.RIGHT]}; "
            elif proxy.right_to_left and alignment in (SE_JC.END, SE_JC.RIGHT):
                algn += f"text-align: {cls.ALGN_TO_ALGN[SE_JC.LEFT]}; "
            else:
                algn += f"text-align: {cls.ALGN_TO_ALGN[alignment]}; "
        elif alignment in cls.ALGN_TO_JSTFY:
            if alignment in cls.ALGN_JSTFIED:
                algn += "text-align: justify;"
            algn += f"text-justify: {cls.ALGN_TO_JSTFY[alignment]}; "
        return algn

    @classmethod
    def _ind(cls, ind: Length | int) -> str:
        if isinstance(ind, Length):
            return f"{ind.pt}pt"
        elif isinstance(ind, int):
            return f"{ind}ch"

    @classmethod
    def _margin(cls, margin: Length | int) -> str:
        if isinstance(margin, Length):
            return f"{margin.pt}pt"
        elif isinstance(margin, int):
            return f"{margin}em"


class HtmlParagraphInList(HtmlParagraph):
    @classmethod
    def element(cls, proxy: Paragraph, ruleset: RuleSet) -> HtmlElement:
        elm = Element(cls.HL_TO_P_TAG[proxy.header_level], cls._attrs(proxy))
        cls._fill_content(proxy, elm, ruleset)
        return elm


class HtmlDrawing(HtmlBuilder["Drawing"]):
    @classmethod
    def element(cls, proxy: Drawing, ruleset: RuleSet) -> HtmlElement:
        return Element("img", cls._attrs(proxy))

    @classmethod
    def _attrs(cls, proxy: Drawing) -> dict[str, str]:
        pic = proxy.picture
        if pic is None:
            return {"width": f"{proxy.width}px", "height": f"{proxy.height}px"}
        base64 = b64encode(pic.resized(proxy.size_px).blob).decode()
        return {"src": f"data:{pic.content_type};base64,{base64}"}


class HtmlListViewInterrupted(HtmlBuilder["ListViewInterrupted"]):
    @classmethod
    def element(
        cls, proxy: ListViewInterrupted, ruleset: RuleSet
    ) -> HtmlElement:
        # docxray stuff
        from docxray.transform.ruleset import Rule

        zero_lst_elm = (
            Element("ul") if proxy.is_bullet_format else Element("ol")
        )
        ruleset_for_p = copy(ruleset)
        ruleset_for_p.set_html_rule("Paragraph", Rule(HtmlParagraphInList))

        def fill_list(up_li: HtmlElement, block: ListViewIlvlBlock) -> None:
            bullet = block.li.is_bullet_format
            lst_elm = Element("ul") if bullet else Element("ol")
            for block_in in block.inside_blocks:
                li_elm = Element("li")
                p_elm: HtmlElement = block_in.li.paragraph.transform(
                    ruleset_for_p, stringify=False
                )
                li_elm.text = p_elm.text
                li_elm.extend(list(p_elm))

                lst_elm.append(li_elm)
                if block_in.inside_blocks:
                    fill_list(li_elm, block_in)
            up_li.append(lst_elm)

        for zero_block in proxy.items_tree:
            zero_li_elm = Element("li")
            p_elm: HtmlElement = zero_block.li.paragraph.transform(
                ruleset_for_p, False
            )
            zero_li_elm.text = p_elm.text
            zero_li_elm.extend(list(p_elm))

            zero_lst_elm.append(zero_li_elm)
            if zero_block.inside_blocks:
                fill_list(zero_li_elm, zero_block)
        return zero_lst_elm


class HtmlTable(HtmlBuilder["Table"]):
    VALIGN_TO_HTML_VALGN = {
        SE_VERTICAL_JC.TOP: "top",
        SE_VERTICAL_JC.CENTER: "middle",
        SE_VERTICAL_JC.BOTTOM: "bottom",
        SE_VERTICAL_JC.BOTH: "middle",
    }
    SE_BORDER_TO_CSS = {
        SE_BORDER.SINGLE: "1px solid black",
        SE_BORDER.THICK: "thick solid black",
        SE_BORDER.DOUBLE: "3px double black",
        SE_BORDER.DOTTED: "2px dotted black",
        SE_BORDER.DASHED: "2px dashed black",
        SE_BORDER.DOT_DASH: "2px dashed black",
        SE_BORDER.DOT_DOT_DASH: "2px dashed black",
        SE_BORDER.TRIPLE: "2px double black;",
        SE_BORDER.THIN_THICK_SMALL_GAP: "thick solid black",
        SE_BORDER.THICK_THIN_SMALL_GAP: "thick solid black",
        SE_BORDER.THIN_THICK_THIN_SMALL_GAP: "thick solid black",
        SE_BORDER.THIN_THICK_MEDIUM_GAP: "3px double black",
        SE_BORDER.THICK_THIN_MEDIUM_GAP: "3px double black",
        SE_BORDER.THIN_THICK_THIN_MEDIUM_GAP: "3px double black",
        SE_BORDER.THIN_THICK_LARGE_GAP: "4px double black",
        SE_BORDER.THICK_THIN_LARGE_GAP: "4px double black",
        SE_BORDER.THIN_THICK_THIN_LARGE_GAP: "4px double black",
        SE_BORDER.WAVE: "3px groove black",
        SE_BORDER.DOUBLE_WAVE: "3px ridge black",
        SE_BORDER.DASH_SMALL_GAP: "2px dashed black",
        SE_BORDER.DASH_DOT_STROKED: "2px dotted black",
        SE_BORDER.THREE_D_EMBOSS: "3px ridge black",
        SE_BORDER.THREE_D_ENGRAVE: "3px groove black",
        SE_BORDER.OUTSET: "3px outset black",
        SE_BORDER.INSET: "3px inset black",
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
            attrs["width"] = units(proxy.width)
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
        sides: set[str] = {"top", "bottom", "left", "right"}
        for side in sides:
            border: str = cls._cell_border(proxy.borders_info[side], side)  # type: ignore[literal-required]
            if border:
                style += f"{border}; "
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
        b = ""
        if (
            border not in (SE_BORDER.NULL, SE_BORDER.NONE)
            and border is not None
        ):
            border_css = (
                cls.SE_BORDER_TO_CSS.get(border.border_type)
                or "1px solid black"
            )
            b = f"border-{side}: {border_css}"
        return b

    @classmethod
    def _cell_padding(cls, proxy: Cell) -> str:
        info = proxy.padding_info
        padding = ""
        sides = {"top", "bottom", "left", "right"}
        for side in sides:
            padding_side = info[side]  # type: ignore[literal-required]
            if padding_side is not None:
                padding += f"padding-{side}: {units(padding_side)}; "
        return padding

    @classmethod
    def _table_attrs(cls, proxy: Table) -> dict[str, str]:
        attrs = {}
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
            style += f"border-spacing: {units(spacing)}; "
        if proxy.left_indent:
            style += f"margin-inline-start: {units(proxy.left_indent)}; "
        return style


class _RunsHtmlBuilder:
    def __init__(
        self,
        paragraph_elm: HtmlElement,
        attr_to_elm_maker: dict[str, ElmMaker],
        ruleset: RuleSet,
    ) -> None:
        self._p_elm = paragraph_elm
        self._attr_elm_map = attr_to_elm_maker
        self._ruleset = ruleset

    def run(self, upper_elm: HtmlElement, run: Run) -> None:
        for item in run.iter_inner_content():
            content: str | HtmlElement | None = None
            if isinstance(item, TxtFragment):
                if run.chars_case is None:
                    content = item.raw
                elif run.chars_case == "up":
                    content = item.raw.upper()
                else:
                    content = item.raw.lower()
            elif isinstance(item, Drawing):
                content = self._img_elm(item)
            elif isinstance(item, Tab):
                content = TAB_MNEMONIC
            else:
                if item.which_break == "textWrapping":
                    content = Element("br")
            if content is not None:
                self._run_content(upper_elm, content)

    def run_chain(self, main: RunChain) -> None:
        main_tag = self._attr_elm_map[main.name](main.comparable)
        between = main.chains_between()
        skip_until: int | None = None
        for idx in range(main.start, main.end + 1):
            if skip_until is not None and idx <= skip_until:
                continue
            main_link = main.link(idx)
            if main_link is None:
                continue
            idxed = self._same_idx_intersects(between, idx)
            if idxed:
                top, bottom = self._chained_tag_tree(idxed)
                exclude = set(idxed) | {main}
                skip_until = self._chained_recursive(
                    bottom, idxed[-1], exclude
                )
                main_tag.append(top)
            else:
                self.run(main_tag, main_link)
        self._run_content(self._p_elm, main_tag)

    def _txt_append(self, element: HtmlElement, txt: str) -> None:
        if element.text is None:
            element.text = txt
        else:
            element.text = element.text + txt

    def _tail_append(self, element: HtmlElement, txt: str) -> None:
        if element.tail is None:
            element.tail = txt
        else:
            element.tail = element.tail + txt

    def _elm_append(
        self, parent_elm: HtmlElement, content: str | HtmlElement
    ) -> None:
        """Append text to parent or append element to parent"""
        if isinstance(content, str):
            self._txt_append(parent_elm, content)
        elif isinstance(content, HtmlElement):
            parent_elm.append(content)

    def _elm_append_child_or_tail(
        self,
        parent_elm: HtmlElement,
        last_child_elm: HtmlElement,
        content: str | HtmlElement,
    ) -> None:
        """Append text to last child else append element to parent."""
        if isinstance(content, str):
            self._tail_append(last_child_elm, content)
        elif isinstance(content, HtmlElement):
            parent_elm.append(content)

    def _last_child(self, element: HtmlElement) -> HtmlElement | None:
        """Get last child of an element. None if it has not."""
        childs = cast("list[HtmlElement]", element.xpath("./*[last()]"))
        if childs:
            return childs[0]
        return None

    def _run_content(
        self, upper_elm: HtmlElement, content: str | HtmlElement
    ) -> None:
        last_child_elm = self._last_child(upper_elm)
        if last_child_elm is None:
            self._elm_append(upper_elm, content)
        else:
            self._elm_append_child_or_tail(upper_elm, last_child_elm, content)

    def _img_elm(self, drawing: Drawing) -> HtmlElement:
        return self._ruleset.html_rules["Drawing"].builder.element(
            drawing, self._ruleset
        )

    def _chained_tag_tree(
        self, indexed: list[RunChain]
    ) -> tuple[HtmlElement, HtmlElement]:
        first = indexed[0]
        top = self._attr_elm_map[first.name](first.comparable)
        bottom = top
        for chain in indexed[1:]:
            elm = self._attr_elm_map[chain.name](chain.comparable)
            bottom.append(elm)
            bottom = elm
        return top, bottom

    def _same_idx_intersects(
        self, between: set[RunChain], idx: int
    ) -> list[RunChain]:
        """Filter by index and topological sorting by length of run chain."""
        return sorted(
            [chain for chain in between if chain.start == idx],
            key=lambda c: len(c),
        )

    def _chained_recursive(
        self,
        bottom: HtmlElement,
        bottom_chain: RunChain,
        exclude: set[RunChain] | None = None,
        skip_until: int = -1,
    ) -> int:
        """Recursively traverses run chains and build up format tag trees.

        Args:
            bottom (_Element): Current bottom element of an format tag tree.
            bottom_chain (RunChain): Current bottom chain.
            exclude (set[RunChain] | None, optional): Exclude processed
                run chains to avoid infinite calls. Defaults to None.
            skip_until (int, optional): Rightmost end index of processed
                run chains. Defaults to -1.

        Returns:
            int: skip_until value.
        """
        between = bottom_chain.chains_between()
        if exclude:
            between = between - exclude
        for idx in range(bottom_chain.start, bottom_chain.end + 1):
            bottom_link = bottom_chain.link(idx)
            if bottom_link is None:
                continue
            idxed = self._same_idx_intersects(between, idx)
            if idxed:
                t, b = self._chained_tag_tree(idxed)
                exclude = set(idxed) | {bottom_chain}
                skip_until = self._chained_recursive(b, idxed[-1], exclude)
                bottom.append(t)
            else:
                self.run(bottom, bottom_link)
            skip_until = idx
        return skip_until
