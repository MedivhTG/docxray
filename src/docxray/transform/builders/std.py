from typing import Any

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.st.enums import (
    SE_TEXT_DIRECTION,
    SE_UNDERLINE,
    SE_VerticalAlignRun,
)

from .types import ElmMaker

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


def pt(length: Length | float) -> str:
    if isinstance(length, Length):
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
