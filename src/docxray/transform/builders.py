from __future__ import annotations

from abc import abstractmethod
from base64 import b64encode
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.proxy.text.run import Run, TxtFragment
from docxray.oxml.trans.st.enums import SE_JC

from .utils.char_graph import RunChain, RunChainsMap

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.text.paragraph import Paragraph

    from .ruleset import RuleSet

T = TypeVar("T")

type ElmMaker = Callable[[str, Any], HtmlElement]


class HtmlBuilder(Generic[T]):
    @classmethod
    @abstractmethod
    def element(cls, proxy: T, ruleset: RuleSet) -> HtmlElement: ...


def toggled_casual_elm(name: str, value: bool) -> HtmlElement:
    if value is False:
        raise ValueError("Value was False when True need")
    if name == "italic":
        return Element("i")
    if name == "bold":
        return Element("b")
    if name == "strike":
        return Element("strike")
    raise ValueError(f"No element for such name {name}")


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
        "strike",
        "underline",
        "vertical_alignment",
    }
    ATTR_TO_ELMMAKER: dict[str, ElmMaker] = {
        "italic": toggled_casual_elm,
        "bold": toggled_casual_elm,
        "strike": toggled_casual_elm,
    }

    @classmethod
    def element(cls, proxy: Paragraph, ruleset: RuleSet) -> HtmlElement:
        elm = Element(cls.HL_TO_P_TAG[proxy.header_level], cls._attrs(proxy))
        cls._fill_content(proxy, elm, ruleset)
        return elm

    @classmethod
    def _fill_content(
        cls, proxy: Paragraph, elm: HtmlElement, ruleset: RuleSet
    ) -> None:
        chain_map = RunChainsMap(cls.ATTR_FOR_MAP)
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
            if isinstance(item, TxtFragment):
                if run.chars_case is None:
                    txt = item.raw
                elif run.chars_case == "up":
                    txt = item.raw.upper()
                else:
                    txt = item.raw.lower()
                self._run_content(upper_elm, txt)
            elif isinstance(item, Drawing):
                img_elm = self._img_elm(item)
                self._run_content(upper_elm, img_elm)
            else:
                if item.which_break == "textWrapping":
                    br_elm = Element("br")
                    self._run_content(upper_elm, br_elm)

    def run_chain(self, main: RunChain) -> None:
        main_tag = self._attr_elm_map[main.name](main.name, main.comparable)
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
        top = self._attr_elm_map[first.name](first.name, first.comparable)
        bottom = top
        for chain in indexed[1:]:
            elm = self._attr_elm_map[chain.name](chain.name, chain.comparable)
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
