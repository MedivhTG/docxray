from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar, cast

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.text.hyperlink import Hyperlink
from docxray.oxml.trans.proxy.text.omath import OMath, OMathParagraph
from docxray.oxml.trans.proxy.text.paragraph import ParaContentProxy
from docxray.oxml.trans.proxy.text.run import Run, Tab, TxtFragment

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.builders.char_graph import RunChain
    from docxray.transform.ruleset import RuleSet

T = TypeVar("T")

type ElmMaker = Callable[[Any], HtmlElement]
TAB_MNEMONIC = "&emsp;"


class HtmlRun:
    def __init__(
        self,
        paragraph_elm: HtmlElement,
        attr_to_elm_maker: dict[str, ElmMaker],
        ruleset: RuleSet,
    ) -> None:
        self._p_elm = paragraph_elm
        self._attr_elm_map = attr_to_elm_maker
        self._ruleset = ruleset

    def content(
        self, upper_elm: HtmlElement, p_content: ParaContentProxy
    ) -> None:
        if isinstance(p_content, Run):
            self.run(upper_elm, p_content)
        elif isinstance(p_content, Hyperlink):
            self.hyperlink(upper_elm, p_content)
        elif isinstance(p_content, OMathParagraph):
            self.omath_para(upper_elm, p_content)

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
                self._content(upper_elm, content)

    def omath_para(
        self, upper_elm: HtmlElement, omath_para: OMathParagraph
    ) -> None:
        self._content(upper_elm, omath_para.transform(self._ruleset, False))

    def omath(self, upper_elm: HtmlElement, omath: OMath) -> None:
        self._content(upper_elm, omath.transform(self._ruleset, False))

    def hyperlink(self, upper_elm: HtmlElement, hyperlink: Hyperlink) -> None:
        for run in hyperlink.iter_inner_content():
            self.run(upper_elm, run)

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
                self.content(main_tag, main_link)
        self._content(self._p_elm, main_tag)

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

    def _content(
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
        self, between: list[RunChain], idx: int
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
            between = [ch for ch in between if ch not in exclude]
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
                self.content(bottom, bottom_link)
            skip_until = idx
        return skip_until
