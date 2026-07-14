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
from docxray.oxml.t.proxy.text.run import (
    CharsCase,
    Run,
    StrikeCase,
    UnderlineInfo,
)
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

from .types import ElmMaker

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


def i_elm(value: bool) -> HtmlElement:
    return Element("i")


def b_elm(value: bool) -> HtmlElement:
    return Element("b")


def strike_elm(value: StrikeCase) -> HtmlElement:
    if value == "single":
        return Element("s")
    return Element(
        "span",
        {
            "style": "text-decoration: line-through; text-decoration-style: double;"
        },
    )


def char_elm(value: CharsCase) -> HtmlElement:
    if value == "caps":
        return Element("span", {"style": "text-transform: uppercase;"})
    return Element("span", {"style": "font-variant: small-caps;"})


def color_elm(value: str) -> HtmlElement:
    return Element("span", {"style": f"color: {value};"})


def underline_elm(value: UnderlineInfo) -> HtmlElement:
    decor = U_DECOR_MAP.get(value["line"])
    if decor is None:
        decor = "underline"
    decor_color = ""
    if value["color"] != "#000000":
        decor_color = f" text-decoration-color: {value["color"]};"
    return Element(
        "span", {"style": f"text-decoration: {decor};{decor_color}"}
    )


def vert_align_elm(value: SE_VERTICAL_ALIGN_RUN) -> HtmlElement:
    if value == SE_VERTICAL_ALIGN_RUN.SUPERSCRIPT:
        return Element("sup")
    return Element("sub")


def pt(length: Length | float) -> str:
    if isinstance(length, Length):
        return f"{length.pt}pt"
    else:
        return f"{length}%"


def tag_tree(
    run_proxy: Any, run_makers: dict[str, ElmMaker]
) -> tuple[HtmlElement, HtmlElement] | None:
    top = None
    bottom = None
    for attr, maker in run_makers.items():
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
    run_makers: dict[str, ElmMaker],
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
    run_makers: dict[str, ElmMaker],
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
