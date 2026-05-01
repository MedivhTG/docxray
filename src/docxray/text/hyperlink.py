from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.text.hyperlink import CT_Hyperlink
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.text.paragraph import Paragraph  # noqa: F401


class Hyperlink(ElementProxy[CT_Hyperlink, "Paragraph"]):
    pass
