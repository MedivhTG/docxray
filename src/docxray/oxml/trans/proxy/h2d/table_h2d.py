from .how_to_display import How2Display
from .table_rslv import CellResolver, RowResolver, TableResolver


class TableH2D(How2Display[TableResolver]):
    pass


class RowH2D(How2Display[RowResolver]):
    pass


class CellH2D(How2Display[CellResolver]):
    pass
