from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.text.paragraph import CT_P
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.blkcntnr import BlockItemContainer  # noqa: F401


class Paragraph(ElementProxy[CT_P, "BlockItemContainer"]):
    pass
