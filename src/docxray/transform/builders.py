from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.st.enums import SE_JC

from .utils.char_graph import RunChain, RunChainsMap

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph

T = TypeVar("T")


class HtmlBuilder(Generic[T]):
    @classmethod
    @abstractmethod
    def element(cls, proxy: T) -> HtmlElement: ...


def toggled_casual_elm(name: str, value: bool):
    if value is False:
        raise ValueError("Value was False when True need")
    if name == "italic":
        return Element("i")
    if name == "bold":
        return Element("b")
    if name == "strike":
        return Element("strike")


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
    ATTR_FOR_MAP = {
        "italic",
        "bold",
        "chars_case",
        "strike",
        "underline",
        "vertical_alignment",
    }
    ATTR_TO_ELM = {
        "italic": toggled_casual_elm,
        "bold": toggled_casual_elm,
        "strike": toggled_casual_elm,
    }

    @classmethod
    def element(cls, proxy: Paragraph) -> HtmlElement:
        elm = Element(cls.HL_TO_P_TAG[proxy.header_level], cls._attrs(proxy))
        # chain_map = cls._fill_content(proxy, elm)
        return elm

    @classmethod
    def _fill_content(cls, proxy: Paragraph, elm: HtmlElement) -> RunChainsMap:
        chain_map = RunChainsMap(cls.ATTR_FOR_MAP)
        for run_or_hlink in proxy.iter_inner_content():
            if isinstance(run_or_hlink, Run):
                chain_map.chain(run_or_hlink)
            else:
                for run in run_or_hlink.iter_inner_content():
                    chain_map.chain(run)
        return chain_map

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
        return style

    @classmethod
    def _alignment(cls, proxy: Paragraph) -> str:
        alignment = proxy.alignment
        algn = ""
        if alignment in cls.ALGN_TO_ALGN:
            algn += f"text-align: {cls.ALGN_TO_ALGN[alignment]}; "
        elif alignment in cls.ALGN_TO_JSTFY:
            if alignment in cls.ALGN_JSTFIED:
                algn += "text-align: justify;"
            algn += f"text-justify: {cls.ALGN_TO_JSTFY[alignment]}; "
        return algn

    @classmethod
    def _ind(cls, ind: Length | int) -> str:
        if isinstance(ind, Length):
            return f"{ind.px()}px"
        elif isinstance(ind, int):
            return f"{ind}ch"


class _RunsBuilder:
    def __init__(
        self, paragraph_elm: HtmlElement, attr_to_elm_maker: Any
    ) -> None:
        self._p_elm = paragraph_elm

    def build(self, chain_map: RunChainsMap):
        for chain in chain_map.chains_ordered():
            pass

    def _chained(self, main: RunChain):
        # In most cases it's enough, but in future do we need eq comparator?
        if not main.comparable:
            return
