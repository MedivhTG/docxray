from collections.abc import Iterator
from functools import cached_property

# docxray stuff
from docxray.blkcntnr import BlockItemContainer
from docxray.enum.word import WD_MERGE
from docxray.oxml.table.table import CT_Row, CT_Tbl, CT_Tc
from docxray.resolver.table import CellResolver, RowResolver, TableResolver
from docxray.shared import (
    ElementProxy,
    PropertyPath,
    StoryChild,
    safe_get_prop,
)


class Cell(BlockItemContainer[CT_Tc]):
    @cached_property
    def resolver(self) -> CellResolver:
        return CellResolver(self.element, self.part.document_part, "")


class Row(ElementProxy[CT_Row]):
    @cached_property
    def resolver(self) -> RowResolver:
        return RowResolver(self.element, self.part, "NO")  # type: ignore[arg-type]

    def iter_cells(self, skip_merged: bool = True) -> Iterator[Cell]:
        for tc_elm in self.element.tc_lst:
            if skip_merged:
                vMerge_val = safe_get_prop(
                    tc_elm, PropertyPath.base("val", "tcPr.vMerge")
                )
                if vMerge_val == WD_MERGE.CONTINUE:
                    continue
            yield Cell(tc_elm, self)  # type: ignore[arg-type]


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def resolver(self) -> TableResolver:
        return TableResolver(self.element, self.part.document_part, "NO")

    def iter_rows(self) -> Iterator[Row]:
        for tr_elm in self.element.tr_lst:
            yield Row(tr_elm, self)
