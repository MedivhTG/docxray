from functools import cached_property

# docxray stuff
from docxray.oxml.table import CT_Tbl
from docxray.resolver.table import TableResolver
from docxray.shared import StoryChild


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def resolver(self) -> TableResolver:
        return TableResolver(self.element, self.part.document_part, "NO")


class Cell:
    pass
