"""Relationship-related objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import Part


class Relationships(dict[str, "_Relationship"]):
    """Collection object for |_Relationship| instances, having list semantics."""

    def __init__(self, baseURI: str) -> None:
        self._baseURI = baseURI
        self._target_parts_by_rId: dict[str, str | Part] = {}

    def add_relationship(
        self,
        reltype: str,
        target: Part | str,
        rId: str,
        is_external: bool = False,
    ) -> "_Relationship":
        """Return a newly added |_Relationship| instance."""
        rel = _Relationship(rId, reltype, target, self._baseURI, is_external)
        self[rId] = rel
        if not is_external:
            self._target_parts_by_rId[rId] = target
        return rel

    def part_with_reltype(self, reltype: str) -> Part:
        """Return target part of rel with matching `reltype`, raising |KeyError| if not
        found and |ValueError| if more than one matching relationship is found.
        """
        rel = self._get_rel_of_type(reltype)
        return rel.target_part

    @property
    def related_parts(self) -> dict[str, Part | str]:
        """Dict mapping rIds to target parts for all the internal relationships in the
        collection."""
        return self._target_parts_by_rId

    def _get_rel_of_type(self, reltype: str) -> _Relationship:
        """Return single relationship of type `reltype` from the collection.

        Raises |KeyError| if no matching relationship is found. Raises |ValueError| if
        more than one matching relationship is found.
        """
        matching = [rel for rel in self.values() if rel.reltype == reltype]
        if len(matching) == 0:
            tmpl = "no relationship of type '%s' in collection"
            raise KeyError(tmpl % reltype)
        if len(matching) > 1:
            tmpl = "multiple relationships of type '%s' in collection"
            raise ValueError(tmpl % reltype)
        return matching[0]


class _Relationship:
    """Value object for relationship to part."""

    def __init__(
        self,
        rId: str,
        reltype: str,
        target: Part | str,
        baseURI: str,
        external: bool = False,
    ) -> None:
        self._rId = rId
        self._reltype = reltype
        self._target = target
        self._baseURI = baseURI
        self._is_external = bool(external)

    @property
    def is_external(self) -> bool:
        return self._is_external

    @property
    def reltype(self) -> str:
        return self._reltype

    @property
    def rId(self) -> str:
        return self._rId

    @property
    def target_part(self) -> Part:
        if self._is_external:
            raise ValueError(
                "target_part property on _Relationship is undefined when target mode is External"
            )
        return cast("Part", self._target)

    @property
    def target_ref(self) -> str:
        if self._is_external:
            return cast(str, self._target)
        else:
            target = cast("Part", self._target)
            return target.partname.relative_ref(self._baseURI)
