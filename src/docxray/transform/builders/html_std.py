from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast
from unicodedata import category

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.proxy.text.hyperlink import Hyperlink
from docxray.oxml.trans.proxy.text.omath import (
    Arg,
    BoxObject,
    OMath,
    OMathParagraph,
    RunOMath,
    TxtFragmentOMath,
)
from docxray.oxml.trans.proxy.text.paragraph import ParaContentProxy
from docxray.oxml.trans.proxy.text.run import Break, Run, Tab, TxtFragment
from docxray.oxml.trans.st.enums import (
    SE_TEXT_DIRECTION,
    SE_UNDERLINE,
    SE_VerticalAlignRun,
)

if TYPE_CHECKING:
    from docxray.transform.ruleset import RuleSet

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


def txt_append(element: HtmlElement, txt: str) -> None:
    if element.text is None:
        element.text = txt
    else:
        element.text = element.text + txt


def tail_append(element: HtmlElement, txt: str) -> None:
    if element.tail is None:
        element.tail = txt
    else:
        element.tail = element.tail + txt


def elm_append(parent_elm: HtmlElement, content: str | HtmlElement) -> None:
    """Append text to parent or append element to parent"""
    if isinstance(content, str):
        txt_append(parent_elm, content)
    elif isinstance(content, HtmlElement):
        parent_elm.append(content)


def elm_append_child_or_tail(
    parent_elm: HtmlElement,
    last_child_elm: HtmlElement,
    content: str | HtmlElement,
) -> None:
    """Append text to last child else append element to parent."""
    if isinstance(content, str):
        tail_append(last_child_elm, content)
    elif isinstance(content, HtmlElement):
        parent_elm.append(content)


def last_child(element: HtmlElement) -> HtmlElement | None:
    """Get last child of an element. None if it has not."""
    childs = cast("list[HtmlElement]", element.xpath("./*[last()]"))
    if childs:
        return childs[0]
    return None


def content_append(upper_elm: HtmlElement, content: str | HtmlElement) -> None:
    last_child_elm = last_child(upper_elm)
    if last_child_elm is None:
        elm_append(upper_elm, content)
    else:
        elm_append_child_or_tail(upper_elm, last_child_elm, content)


def txt(run: Run, txt_fgmt: TxtFragment) -> str:
    if run.chars_case is None:
        return txt_fgmt.raw
    elif run.chars_case == "up":
        return txt_fgmt.raw.upper()
    else:
        return txt_fgmt.raw.lower()


def break_elm(br: Break) -> HtmlElement | None:
    if br.break_type == "textWrapping":
        return Element("br")
    return None


def tab(tab: Tab) -> str:
    return TAB_MNEMONIC


def run(upper_elm: HtmlElement, run: Run, ruleset: RuleSet) -> None:
    for item in run.iter_inner_content():
        content: str | HtmlElement | None = None
        if isinstance(item, TxtFragment):
            content = txt(run, item)
        elif isinstance(item, Drawing):
            content = drawing(item, ruleset)
        elif isinstance(item, Tab):
            content = tab(item)
        else:
            content = break_elm(item)
        if content is not None:
            content_append(upper_elm, content)


def is_math_op(chr: str) -> bool:
    return category(chr) == "Sm"


def txt_elm_omath(txt_fgmt: TxtFragmentOMath | TxtFragment) -> HtmlElement:
    def _mo_elm(txt: str) -> HtmlElement:
        mo_elm = Element("mo")
        mo_elm.text = txt
        return mo_elm

    as_op = False
    if isinstance(txt_fgmt._parent, Arg):
        if isinstance(txt_fgmt._parent._parent, BoxObject):
            box = txt_fgmt._parent._parent
            if box.emulate_operator:
                as_op = True
    mrow_elm = Element("mrow")
    elms: list[HtmlElement] = []
    if as_op:
        elms.append(_mo_elm(txt_fgmt.raw))
    else:
        for chr in txt_fgmt.raw:
            elm = Element("mo") if is_math_op(chr) else Element("mi")
            elm.text = chr
            elms.append(elm)
    for elm in elms:
        # Only for OMath elements cause of Readability in HTML -
        # even with one space it will be collapsed
        if txt_fgmt.preserve:
            elm.set("style", "white-space: pre-wrap;")
        mrow_elm.append(elm)
    return mrow_elm


def run_omath(upper_elm: HtmlElement, run: RunOMath, ruleset: RuleSet) -> None:
    for item in run.iter_inner_content():
        content: str | HtmlElement | None = None
        if isinstance(item, (TxtFragmentOMath, TxtFragment)):
            content = txt_elm_omath(item)
        elif isinstance(item, Drawing):
            content = drawing(item, ruleset)
        elif isinstance(item, Tab):
            content = tab(item)
        else:
            content = break_elm(item)
        if content is not None:
            content_append(upper_elm, content)


def hyperlink(
    upper_elm: HtmlElement, hyperlink: Hyperlink, ruleset: RuleSet
) -> None:
    for run_proxy in hyperlink.iter_inner_content():
        run(upper_elm, run_proxy, ruleset)


def drawing(drawing: Drawing, ruleset: RuleSet) -> HtmlElement:
    return drawing.transform(ruleset, False)


def omath_para(
    upper_elm: HtmlElement, omath_para: OMathParagraph, ruleset: RuleSet
) -> None:
    content_append(upper_elm, omath_para.transform(ruleset, False))


def omath(upper_elm: HtmlElement, omath: OMath, ruleset: RuleSet) -> None:
    content_append(upper_elm, omath.transform(ruleset, False))


def paragraph_content(
    upper_elm: HtmlElement, p_content: ParaContentProxy, ruleset: RuleSet
) -> None:
    if isinstance(p_content, Run):
        run(upper_elm, p_content, ruleset)
    elif isinstance(p_content, Hyperlink):
        hyperlink(upper_elm, p_content, ruleset)
    elif isinstance(p_content, OMathParagraph):
        omath_para(upper_elm, p_content, ruleset)
    elif isinstance(p_content, OMath):
        omath(upper_elm, p_content, ruleset)
