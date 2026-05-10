from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.h2d.table_h2d import CellH2D
from docxray.oxml.trans.proxy.table import Cell

from .how_to_display import How2Display
from .paragraph_rslv import ParagraphResolver


class ParagraphH2D(How2Display[ParagraphResolver]):
    @cached_property
    def cell_h2d(self) -> CellH2D | None:
        container = self._rslvr._proxy.container
        if isinstance(container, Cell):
            return container.h2d
        return None
