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
from docxray.oxml.t.proxy.text.paragraph import ParaContentProxy
from docxray.oxml.t.proxy.text.run import Break, Run, Tab, TxtFragment
from docxray.oxml.t.proxy.types import StrikeCase, UnderlineInfo
from docxray.oxml.t.st.enums import (
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


def strike_elm(value: StrikeCase) -> HtmlElement:
    if value == "single":
        return Element("s")
    return Element(
        "span",
        {
            "style": "text-decoration: line-through; text-decoration-style: double;"
        },
    )


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


def txt(run: Run, txt_fgmt: TxtFragment) -> str | HtmlElement:
    if run.chars_case is None:
        return txt_fgmt.raw
    elif run.chars_case == "caps":
        return Element("span", {"style": "text-transform: uppercase;"})
    else:
        return Element("span", {"style": "font-variant: small-caps;"})


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


__OFFICE_MATH_RUN_PROCESS_ORIGIN_FUNC = OfficeMathRun.process


# TODO: look for other content process
def omath_to_latex(
    omath: OMath,
    ruleset: RuleSet | None = None,
    include_run_content: bool = True,
) -> str:
    # docxray stuff
    from docxray.oxml.t.parts.document import DocumentPart

    ruleset = ruleset or cast("DocumentPart", omath.part)._default_html_ruleset

    def _drawing_latex(drawing: Drawing) -> str:
        img_elm: HtmlElement = drawing.transform(ruleset, False)
        src = img_elm.get("src")
        if src:
            background = f"background: url('{src}') no-repeat center; background-size: contain;"
        else:
            background = ""
        width_px = drawing.width.px()
        height_px = drawing.height.px()
        return f"\\style{{display: inline-block; width: {width_px}px; height: {height_px}px; {background}}}{{}}"

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
                text_content = (el.text or "").strip()
                if el.get(qname("xml", "space")) == "preserve":
                    math_string += (
                        "\\ \\ "
                        if text_content == ""
                        else OfficeMathFieldCodeText(text_content).process(
                            chr_
                        )
                    )
                else:
                    math_string += (
                        text_content.replace("_", "\\_")
                        .replace("^", "\\^")
                        .replace("{", "\\{")
                        .replace("}", "\\}")
                    )
            elif el.tag == qname("w", "drawing"):
                math_string += _drawing_latex(
                    Drawing(el, omath)  # pyright: ignore[reportArgumentType]
                )

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
    return process_math_node(omath.element)


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
