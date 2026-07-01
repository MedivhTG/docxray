from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.proxy.table import Cell
from docxray.oxml.trans.st.enums import (
    SE_JC,
    SE_LEVEL_SUFFIX,
    SE_LINE_SPACING_RULE,
)

from .base import HtmlBuilder
from .char_graph import RunChain, RunChainsMap
from .run import HtmlRun

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.table import Cell
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph
    from docxray.transform.ruleset import RuleSet

from .html_std import (
    SPACEBREAK_MNEMONIC,
    TAB_MNEMONIC,
    TEXT_FLOW_TO_WRITING_MODE,
    b_elm,
    i_elm,
    paragraph_content,
    strike_elm,
    tag_tree,
    underline_elm,
    vert_align_elm,
)
from .types import ElmMaker


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
    ALGN_MAP = {
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
        if (
            not proxy.has_text
            and not proxy.has_picture
            and not proxy.list_item
        ):
            elm.text = SPACEBREAK_MNEMONIC
            return
        chain_map = RunChainsMap(list(cls.ATTR_TO_ELMMAKER))
        for item in proxy.iter_inner_content():
            chain_map.chain(item)
        runs_builder = HtmlRun(elm, cls.ATTR_TO_ELMMAKER, ruleset)
        for unchained_or_chain in chain_map.chains_ordered():
            if isinstance(unchained_or_chain, RunChain):
                runs_builder.run_chain(unchained_or_chain)
            else:
                paragraph_content(elm, unchained_or_chain, ruleset)

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
        in_table = isinstance(proxy.container, Cell)
        if proxy.margin_line_start:
            style += f"margin-inline-start: {cls._ind(proxy.margin_line_start, in_table)}; "
        if proxy.margin_line_end:
            style += f"margin-inline-end: {cls._ind(proxy.margin_line_end, in_table)}; "
        if proxy.text_indent:
            style += f"text-indent: {cls._ind(proxy.text_indent, in_table)}; "
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
        if h2d.word_wrap:
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
        if alignment in cls.ALGN_MAP:
            if proxy.right_to_left and alignment in (SE_JC.START, SE_JC.LEFT):
                algn += f"text-align: {cls.ALGN_MAP[SE_JC.RIGHT]}; "
            elif proxy.right_to_left and alignment in (SE_JC.END, SE_JC.RIGHT):
                algn += f"text-align: {cls.ALGN_MAP[SE_JC.LEFT]}; "
            else:
                algn += f"text-align: {cls.ALGN_MAP[alignment]}; "
        elif alignment in cls.ALGN_TO_JSTFY:
            if alignment in cls.ALGN_JSTFIED:
                algn += "text-align: justify;"
            algn += f"text-justify: {cls.ALGN_TO_JSTFY[alignment]}; "
        return algn

    @classmethod
    def _ind(cls, ind: Length | int, in_table: bool) -> str:
        if isinstance(ind, Length):
            if in_table:
                return "0pt"
            else:
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
