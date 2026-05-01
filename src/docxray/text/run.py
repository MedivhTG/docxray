from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.text.run import CT_R
from docxray.shared import ElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray.text.paragraph import Paragraph  # noqa: F401


class Run(ElementProxy[CT_R, "Paragraph"]):
    @cached_property
    def raw_text(self) -> str:
        t_elm = self.element.t
        if t_elm is None:
            return ""
        return t_elm.txt
