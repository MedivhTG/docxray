from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

from lxml.html import HtmlElement

from .html_std import content_append, paragraph_content

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
                paragraph_content(main_tag, main_link, self._ruleset)
        content_append(self._p_elm, main_tag)

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
                paragraph_content(bottom, bottom_link, self._ruleset)
            skip_until = idx
        return skip_until
