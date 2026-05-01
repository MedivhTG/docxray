from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.table import CT_Tbl
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.blkcntnr import BlockItemContainer  # noqa: F401


class Table(ElementProxy[CT_Tbl, "BlockItemContainer"]):
    pass


class Cell:
    pass
