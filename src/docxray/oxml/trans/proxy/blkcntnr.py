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
    from docxray.oxml.trans.h2d.paragraph import ListView
    from docxray.oxml.trans.proxy.table import Table

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

    def iter_inner_contet_with_lists(
        self,
    ) -> Iterator[Paragraph | ListView | Table]:
        """Iterate over content in container with `ListView` additionaly.

        `NOTE`: lists contain only paragraphs as list items, but Word
        has cases with paragraphs/tables between list items, so if you want get it -
        inspect this list by checking property `next_content_item` or
        `prev_content_item` with `list_item` while iterating over list items.
        """
        # docxray stuff
        from docxray.oxml.trans.proxy.table import Table

        num_id_skip = None
        for item in self.inner_content:
            if isinstance(item, Table):
                yield item
            else:
                list_view = item.list_view
                if list_view is None:
                    yield item
                else:
                    if num_id_skip == list_view._li.num_id:
                        continue
                    num_id_skip = list_view._li.num_id
                    yield list_view
