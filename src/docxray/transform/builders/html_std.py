from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from lxml.html import Element, HtmlElement
from officemath2latex import (
    OfficeMathFieldCodeText,
    OfficeMathRun,
    process_math_node,
    qname,
)

# docxray stuff
from docxray.length import Length
from docxray.oxml.t.proxy.drawing import Drawing
from docxray.oxml.t.proxy.text.hyperlink import Hyperlink
from docxray.oxml.t.proxy.text.omath import OMath, OMathParagraph
from docxray.oxml.t.proxy.text.paragraph import PContent
from docxray.oxml.t.proxy.text.run import Run
from docxray.oxml.t.proxy.text.run_content import (
    Break,
    CarriageReturn,
    NonBreakHyphen,
    OptionalHyphen,
    Separator,
    Symbol,
    Tab,
    TxtFragment,
)
from docxray.oxml.t.st.enums import (
    SE_TEXT_DIRECTION,
    SE_UNDERLINE,
    SE_VERTICAL_ALIGN_RUN,
)

if TYPE_CHECKING:
    from docxray.transform.ruleset import RuleSet
    from docxray.oxml.t.proxy.text.list import ListItem

from .types import RunMaker

TAB = "&emsp;"
SPACEBREAK = "&nbsp;"
NON_BREAK_HYPHEN = "&#8209;"
SOFT_HYPHEN = "&shy;"
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
    SE_UNDERLINE.WAVY_DOUBLE: "underline wavy",
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


def i_elm(proxy: Run | ListItem) -> HtmlElement | None:
    if proxy.character_format.italic:
        return Element("i")
    return None


def b_elm(proxy: Run | ListItem) -> HtmlElement | None:
    if proxy.character_format.bold:
        return Element("b")
    return None


def vert_align_elm(proxy: Run | ListItem) -> HtmlElement | None:
    if proxy.character_format.vertical_alignment is None:
        return None
    valign = proxy.character_format.vertical_alignment
    if valign == SE_VERTICAL_ALIGN_RUN.SUPERSCRIPT:
        return Element("sup")
    return Element("sub")


def underline_elm(proxy: Run | ListItem) -> HtmlElement | None:
    if proxy.character_format.underline_info is None:
        return None
    u_inf = proxy.character_format.underline_info
    decor = U_DECOR_MAP.get(u_inf["line"])
    if decor is None:
        decor = "underline"
    decor_color = ""
    if u_inf["color"] != "#000000":
        decor_color = f" text-decoration-color: {u_inf["color"]};"
    return Element(
        "span", {"style": f"text-decoration: {decor};{decor_color}"}
    )


def format_run_elm(proxy: Run | ListItem) -> HtmlElement | None:
    span_elm: HtmlElement | None = None
    style = ""
    ch_fmt = proxy.character_format
    if ch_fmt.hide_text:
        style += "display: none; "
    if ch_fmt.strike_case:
        strike = ch_fmt.strike_case
        line = "text-decoration: line-through; "
        if strike == "single":
            style += line
        else:
            style += f"{line}text-decoration-style: double; "
    if ch_fmt.font and isinstance(proxy, Run):
        txt = proxy.raw_text.strip()
        if txt:
            font = ch_fmt.font.guess_font(txt[0], default="")
            if font:
                style += f"font-family: {font}; "
    if ch_fmt.chars_case:
        ch = ch_fmt.chars_case
        if ch == "caps":
            style += "text-transform: uppercase; "
        else:
            style += "font-variant: small-caps; "
    if ch_fmt.font_size is not None:
        style += f"font-size: {ch_fmt.font_size.pt}pt; "
    if ch_fmt.font_kerning is not None:
        if (
            ch_fmt.font_size is not None
            and ch_fmt.font_size >= ch_fmt.font_kerning
        ):
            style += "font-kerning: normal; "
    if ch_fmt.color != "#000000":
        style += f"color: {ch_fmt.color}; "
    if ch_fmt.highlight:
        style += f"background-color: {ch_fmt.highlight}; "
    if ch_fmt.text_scale != 100:
        if ch_fmt.text_scale > 100:
            mode = "grow"
        else:
            mode = "shrink"
        style += f"text-fit: {mode} {ch_fmt.text_scale}%; "
    if ch_fmt.letter_spacing is not None:
        style += f"letter-spacing: {ch_fmt.letter_spacing.pt}pt; "
    if ch_fmt.vertical_offset:
        style += f"position: relative; top: {-ch_fmt.vertical_offset.pt}pt; "
    if style:
        span_elm = Element("span", {"style": style})
    return span_elm


RUN_MAKERS_DEFAULT: list[RunMaker] = [
    i_elm,
    b_elm,
    vert_align_elm,
    underline_elm,
    format_run_elm,
]


def pt(length: Length | float) -> str:
    if isinstance(length, Length):
        return f"{length.pt}pt"
    else:
        return f"{length}%"


def tag_tree(
    run_proxy: Any, run_makers: list[RunMaker]
) -> tuple[HtmlElement, HtmlElement] | None:
    top = None
    bottom = None
    for maker in run_makers:
        elm = maker(run_proxy)
        if elm is None:
            continue
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


def txt(txt_fgmt: TxtFragment) -> str | HtmlElement:
    if txt_fgmt.txt_type != "t":
        return ""
    txt = txt_fgmt.raw
    if txt_fgmt.preserve:
        elm = Element("span", {"style": "white-space: pre-wrap;"})
        elm.text = txt
        return elm
    return txt


def break_elm(br: Break) -> HtmlElement | None:
    if br.break_type == "textWrapping":
        return Element("br")
    return None


def tab(tab: Tab) -> str:
    return TAB


def non_br_hyphen(hyphen: NonBreakHyphen) -> str:
    return NON_BREAK_HYPHEN


def soft_hyphen(hyphen: OptionalHyphen) -> str:
    return SOFT_HYPHEN


def carriage_return(cr: CarriageReturn) -> HtmlElement:
    return Element("br")


def separator(sep: Separator) -> HtmlElement:
    return Element("hr")


def symbol(sym: Symbol) -> HtmlElement | str:
    if sym.font is None:
        return sym.character
    elm = Element("span", {"style": f"font-family: {sym.font};"})
    elm.text = sym.character
    return elm


def run(
    upper_elm: HtmlElement,
    run: Run,
    run_makers: list[RunMaker],
    ruleset: RuleSet,
) -> None:
    tree = tag_tree(run, run_makers)
    if tree is not None:
        top, bottom = tree
        upper_elm.append(top)
        upper_elm = bottom
    for item in run.iter_inner_content():
        content: str | HtmlElement | None = None
        if isinstance(item, TxtFragment):
            content = txt(item)
        elif isinstance(item, Drawing):
            content = drawing(item, ruleset)
        elif isinstance(item, Tab):
            content = tab(item)
        elif isinstance(item, Break):
            content = break_elm(item)
        elif isinstance(item, Symbol):
            content = symbol(item)
        elif isinstance(item, NonBreakHyphen):
            content = non_br_hyphen(item)
        elif isinstance(item, OptionalHyphen):
            content = soft_hyphen(item)
        elif isinstance(item, CarriageReturn):
            content = carriage_return(item)
        elif isinstance(item, Separator):
            content = separator(item)
        if content is not None:
            content_append(upper_elm, content)


__OFFICE_MATH_RUN_PROCESS_ORIGIN_FUNC = OfficeMathRun.process


def omath_to_mathjax(
    omath: OMath,
    ruleset: RuleSet | None = None,
    include_run_content: bool = True,
) -> str:
    # docxray stuff
    from docxray.oxml.t.parts.document import DocumentPart

    ruleset = ruleset or cast("DocumentPart", omath.part)._default_html_ruleset

    def _drawing(drawing: Drawing) -> str:
        img_elm: HtmlElement = drawing.transform(ruleset, False)
        src = img_elm.get("src")
        if src:
            background = f"background: url('{src}') no-repeat center; background-size: contain;"
        else:
            background = ""
        width_px = drawing.width.px()
        height_px = drawing.height.px()
        return f"\\style{{display: inline-block; width: {width_px}px; height: {height_px}px; {background}}}{{}}"

    def _sym(sym: Symbol) -> str:
        font = sym.font or ""
        return f"\\unicode[{font}]{{{ord(sym.character)}}}"

    def _nb_hyphen() -> str:
        return f"\\text{{{NON_BREAK_HYPHEN}}}"

    def _soft_hyphen() -> str:
        return f"\\text{{{SOFT_HYPHEN}}}"

    def _process_run(self: OfficeMathRun, chr_: str = "") -> str:
        replacements = [
            (r"π", r"\pi "),
            (r"∞", r"\infty "),
            (r"→", r"\rightarrow "),
            (r"±", r"\pm "),
            (r"∓", r"\mp "),
            (r"α", r"\alpha "),
            (r"β", r"\beta "),
            (r"γ", r"\gamma "),
            (r"…", r"\ldots "),
            (r"⋅", r"\cdot "),
            (r"×", r"\times "),
            (r"θ", r"\theta "),
            (r"Γ", r"\Gamma "),
            (r"≈", r"\approx "),
            (r"ⅈ", r"i "),
            (r"∇", r"\nabla "),
            (r"ⅆ", r"d "),
            (r"≥", r"\geq "),
            (r"∀", r"\forall "),
            (r"∃", r"\exists "),
            (r"∧", r"\land "),
            (r"⇒", r"\Rightarrow "),
            (r"ψ", r"\psi "),
            (r"∂", r"\partial "),
            (r"≠", r"\neq "),
            (r"~", r"\sim "),
            (r"÷", r"\div "),
            (r"∝", r"\propto "),
            (r"≪", r"\ll "),
            (r"≫", r"\gg "),
            (r"≤", r"\leq "),
            (r"≅", r"\cong "),
            (r"≡", r"\equiv "),
            (r"∁", r"\complement "),
            (r"∪", r"\cup "),
            (r"∩", r"\cap "),
            (r"∅", r"\varnothing "),
            (r"∆", r"\mathrm{\\Delta} "),
            (r"∄", r"\nexists "),
            (r"∈", r"\in "),
            (r"∋", r"\ni "),
            (r"←", r"\leftarrow "),
            (r"↑", r"\uparrow "),
            (r"↓", r"\downarrow "),
            (r"↔", r"\leftrightarrow "),
            (r"∴", r"\therefore "),
            (r"¬", r"\neg "),
            (r"δ", r"\delta "),
            (r"ε", r"\varepsilon "),
            (r"ϵ", r"\epsilon "),
            (r"ϑ", r"\vartheta "),
            (r"μ", r"\mu "),
            (r"ρ", r"\rho "),
            (r"σ", r"\sigma "),
            (r"τ", r"\tau "),
            (r"φ", r"\varphi "),
            (r"ω", r"\omega "),
            (r"∙", r"\bullet "),
            (r"⋮", r"\vdots "),
            (r"⋱", r"\ddots "),
            (r"ℵ", r"\aleph "),
            (r"ℶ", r"\beth "),
            (r"∎", r"\blacksquare "),
            (r"%°", r"\%{^\\circ} "),
            (r"√", r"\sqrt{} "),
            (r"∛", r"\sqrt[3]{} "),
            (r"∜", r"\sqrt[4]{} "),
            (r"≜", r"\triangleq "),
            (r"<", r"\lt "),
            (r">", r"\gt "),
            (r"|", r"\mid "),
            (r"∣", r"\mid "),
        ]

        math_string = ""
        flag_bold = False
        for el in self.node:
            if el.tag == qname("m", "rPr"):
                for rpr in el:
                    if (
                        rpr.tag == qname("m", "sty")
                        and rpr.get(qname("m", "val")) == "b"
                    ):
                        flag_bold = True
            elif el.tag == qname("m", "t"):
                text_content = el.text or ""
                if el.get(qname("xml", "space")) == "preserve":
                    pre = (
                        "\\ \\ "
                        if text_content == ""
                        else OfficeMathFieldCodeText(text_content).process(
                            chr_
                        )
                    )
                    # Spaces in Word
                    math_string += pre.replace(" ", r"\,")
                else:
                    pre = (
                        text_content.strip()
                        .replace("_", "\\_")
                        .replace("^", "\\^")
                        .replace("{", "\\{")
                        .replace("}", "\\}")
                    )
                    # Spaces in Word
                    math_string += pre.replace(" ", r"\,")
            elif el.tag == qname("w", "drawing"):
                math_string += _drawing(
                    Drawing(el, omath)  # pyright: ignore[reportArgumentType]
                )
            elif el.tag == qname("w", "sym"):
                math_string += _sym(
                    Symbol(el, omath)  # pyright: ignore[reportArgumentType]
                )
            elif el.tag == qname("w", "noBreakHyphen"):
                math_string += _nb_hyphen()
            elif el.tag == qname("w", "softHyphen"):
                math_string += _soft_hyphen()

        for pre, post in replacements:
            math_string = math_string.replace(pre, post)

        if flag_bold:
            math_string = f"\\mathbf{{{math_string}}}"
        return math_string

    if include_run_content:
        # MonkeyPatch (external lib can't parse run content)
        OfficeMathRun.process = _process_run
    else:
        OfficeMathRun.process = __OFFICE_MATH_RUN_PROCESS_ORIGIN_FUNC
    return f"\\[{process_math_node(omath.element)}\\]"


def hyperlink(
    upper_elm: HtmlElement, hyperlink: Hyperlink, ruleset: RuleSet
) -> None:
    content_append(upper_elm, hyperlink.transform(ruleset, False))


def drawing(drawing: Drawing, ruleset: RuleSet) -> HtmlElement:
    return drawing.transform(ruleset, False)


def omath_para(
    upper_elm: HtmlElement, omath_para: OMathParagraph, ruleset: RuleSet
) -> None:
    content_append(upper_elm, omath_para.transform(ruleset, False))


def omath(upper_elm: HtmlElement, omath: OMath, ruleset: RuleSet) -> None:
    content_append(upper_elm, omath.transform(ruleset, False))


def paragraph_content(
    upper_elm: HtmlElement,
    p_content: PContent,
    run_makers: list[RunMaker],
    ruleset: RuleSet,
) -> None:
    if isinstance(p_content, Run):
        run(upper_elm, p_content, run_makers, ruleset)
    elif isinstance(p_content, Hyperlink):
        hyperlink(upper_elm, p_content, ruleset)
    elif isinstance(p_content, OMathParagraph):
        omath_para(upper_elm, p_content, ruleset)
    elif isinstance(p_content, OMath):
        omath(upper_elm, p_content, ruleset)
