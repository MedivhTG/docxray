from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.st.enums import SE_JC

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph

T = TypeVar("T")


class HtmlBuilder(Generic[T]):
    @classmethod
    @abstractmethod
    def element(cls, proxy: T) -> HtmlElement: ...


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

    @classmethod
    def element(cls, proxy: Paragraph) -> HtmlElement:
        return Element(cls.HL_TO_P_TAG[proxy.header_level], cls._attrs(proxy))

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
