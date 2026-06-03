from __future__ import annotations

from collections.abc import Iterator
from typing import Any

# docxray stuff
from docxray.oxml.trans.proxy.text.run import Run

# docx_tools stuff


class RunChainsMap:
    """Support class for `CharacterFormat` mapping in `Run`.

    This class uses partially interval graphs to merge consecutive tags,
    e.g.: `<i>te</i><i>xt</i>` into `<i>text</i>`. Works with nested
    tags too.

    It was needed in purpose that Word formats parts of a paragraph as
    runs and they all has separate character format.

    Unchained runs are runs without formating (common text).
    """

    def __init__(self, attrs_for_map: set[str]) -> None:
        self._tags_for_map = attrs_for_map
        self._idx_chains: dict[int, dict[str, RunChain]] = {}
        self._unchained: dict[int, Run] = {}
        self._last_idx = -1

    def __len__(self) -> int:
        """Length of run formatting index-axis."""
        return self._last_idx + 1

    def chain(self, run: Run) -> None:
        """Add format chains for this run wrapper.

        We try ty continue one char format (e.g. italic) as chain.
        If chain at last index is not found than we create new named chain.

        If run has no formatting than it's appended to unchained list.

        Args:
            run (Run): Chained run wrapper.
        """
        new_idx = self._last_idx + 1
        self._create_idx(new_idx)
        # Flag for chained or unchained char format
        is_chained = False
        # Iterate over all char format attributes
        for name in self._tags_for_map:
            attr = getattr(run, name)
            # Boolean comparator?
            if not attr:
                continue
            is_chained = True
            chain = self.get_chain(self._last_idx, name)
            if not chain:
                # New chain
                chain = RunChain(name, attr, new_idx)
                chain.append(run)
                self._index_chain(new_idx, chain)
            else:
                if chain.compare(attr):
                    # Continue last chain
                    chain.append(run)
                    self._index_chain(new_idx, chain)
                # If value of attribute is different -> start new chain
                else:
                    chain = RunChain(name, attr, new_idx)
                    chain.append(run)
                    self._index_chain(new_idx, chain)
        if is_chained:
            self._add_chain_intersections(new_idx)
        else:
            self._index_unchained(new_idx, run)
        self._last_idx = new_idx

    def chains_ordered(self) -> Iterator[Run | RunChain]:
        """Iterate over the longest run chains or run wrappers by index.

        For every index we get unchained format or main chain - chain with
        the smallest start index and longest length.
        """
        chains_seen: set[RunChain] = set()

        for i in range(len(self)):
            unchained = self.get_unchained(i)
            if unchained is not None:
                yield unchained
                continue
            for name in self._tags_for_map:
                chain = self.get_chain(i, name)
                if chain is None or chain in chains_seen:
                    continue
                all = {chain}
                all.update(chain.intersections)
                all_remained = all - chains_seen
                # Topological sorting by start index
                all_sorted = sorted(
                    all_remained, key=lambda c: (c.start, len(c))
                )
                chains_seen.update(all_sorted)
                yield all_sorted[0]

    def get_chain(self, idx: int, name: str) -> RunChain | None:
        """Get chain by index and attribute chain name."""
        idx_chains = self._idx_chains.get(idx)
        if not idx_chains:
            return None
        return idx_chains.get(name)

    def get_unchained(self, idx: int) -> Run | None:
        """Get unchained run wrapper by index."""
        return self._unchained.get(idx)

    def _create_idx(self, idx: int) -> None:
        """Create space for new index in interval."""
        self._idx_chains[idx] = {}

    def _index_unchained(self, idx: int, run: Run) -> None:
        """Index unchained run wrapper in interval."""
        self._unchained[idx] = run

    def _index_chain(self, idx: int, chain: RunChain) -> None:
        """Index chain in interval."""
        self._idx_chains[idx][chain.name] = chain

    def _add_chain_intersections(self, idx: int) -> None:
        """Add references for format edges as graph intersections.

        Let's assume that a run chain is a vertex in a graph,
        and all chains that intersect with another chain by index
        form edges (connections), they are all bidirectional.

        Example with chains at current idx=3:

        INTERVALS: 1-2-3-4-5-6-7

        bold: 1-2-3-4-5

        italic: 1-2-3-4 ... 6-7

        underline: 2-3-4-5-6-7

        Chains presented as numbers with hyphens
        (one number - one link in chain).
        Ellipsis is break between different chains in one name (e.g. italic).

        GRAPH at idx=3:

            bold ◄────► italic
              ╲         ╱
               ╲       ╱
                ╲     ╱
                underline
        """
        attrs_remained = self._tags_for_map.copy()
        for name in self._tags_for_map:
            chain = self.get_chain(idx, name)
            if chain is None:
                attrs_remained.discard(name)
                continue
            attrs_to_check = attrs_remained - {name}
            for subname in attrs_to_check:
                subchain = self.get_chain(idx, subname)
                if subchain is None:
                    continue
                chain.add_intersection(subchain)
                subchain.add_intersection(chain)
            attrs_remained.discard(name)


class RunChain:
    def __init__(self, name: str, attr: Any, start: int) -> None:
        self._name = name
        self._comparable = attr
        self._links: dict[int, Run] = {}
        self._start = start
        self.__intersections: set[RunChain] = set()

    def __len__(self) -> int:
        """Length of chain in single run chain."""
        return self._links.__len__()

    @property
    def name(self) -> str:
        """Name of character format attribute."""
        return self._name

    @property
    def start(self) -> int:
        """Start index."""
        return self._start

    @property
    def end(self) -> int:
        """End index."""
        return self._start + self.__len__() - 1

    @property
    def intersections(self) -> set[RunChain]:
        """Run chain references inetersected."""
        return self.__intersections

    @property
    def links(self) -> list[Run]:
        """Run wrappers linked in current chain."""
        return list(self._links.values())

    @property
    def comparable(self) -> Any:
        return self._comparable

    def add_intersection(self, chain: RunChain) -> None:
        """Add new intersection."""
        self.__intersections.add(chain)

    def in_range_of(self, upper: RunChain) -> bool:
        """If current chain between indexes of upper chain."""
        return self.start >= upper.start and self.end <= upper.end

    def chains_between(self) -> set[RunChain]:
        """All chains that between current from intersections.

        It is determined using the start and end indexes.
        """
        chains_inside = set()
        for intersection in self.intersections:
            if intersection.in_range_of(self):
                chains_inside.add(intersection)
        return chains_inside

    def link(self, idx: int) -> Run | None:
        """Get link by index."""
        return self._links.get(idx)

    def append(self, run: Run) -> None:
        """Append new link."""
        self._links[self.end + 1] = run

    def compare(self, comparable: Any) -> bool:
        return comparable == self._comparable
