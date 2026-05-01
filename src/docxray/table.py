from functools import cached_property

# docxray stuff
from docxray.format.table import TableFormat
from docxray.oxml.table import CT_Tbl
from docxray.shared import StoryChild


class Table(StoryChild[CT_Tbl]):
    @cached_property
    def fmt(self) -> TableFormat:
        return TableFormat(self.element, self.part.document_part, "NO")


class Cell:
    pass
