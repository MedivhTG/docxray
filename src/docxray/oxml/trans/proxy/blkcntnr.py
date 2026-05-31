"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, TypeVar

# docxray stuff
from docxray.oxml.trans.document import CT_Body
from docxray.oxml.trans.proxy.shared import StoryChild
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.table.table import CT_Tc
from docxray.oxml.trans.text.paragraph import CT_P

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.table import Table
    from docxray.oxml.trans.h2d.list_view import ListViewInterrupted

type _BlockItemElement = CT_Body | CT_Tc

BLCK_ITEM_ELM_T = TypeVar("BLCK_ITEM_ELM_T", bound=_BlockItemElement)


class BlockItemContainer(StoryChild[BLCK_ITEM_ELM_T]):
    @cached_property
    def inner_content(self) -> list[Paragraph | Table]:
        # docxray stuff
        from docxray.oxml.trans.proxy.table import Table

        content: list[Paragraph | Table] = []
        for element in self._element.inner_content_elements:
            if isinstance(element, CT_P):
                content.append(Paragraph(element, self))
            else:
                content.append(Table(element, self))
        return content

    def iter_inner_content(self) -> Iterator[Paragraph | Table]:
        for item in self.inner_content:
            yield item

    def iter_inner_content_with_lists(
        self,
    ) -> Iterator[Paragraph | Table | ListViewInterrupted]:
        skip_list_until = None
        for item in self.inner_content:
            if (
                skip_list_until is not None
                and item.content_idx <= skip_list_until
            ):
                continue
            if isinstance(item, Table):
                yield item
            else:
                if item.list_view_interrupted is not None:
                    skip_list_until = item.list_view_interrupted.list_ends
                    yield item.list_view_interrupted
                else:
                    yield item
