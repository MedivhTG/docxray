from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.text.hyperlink import CT_Hyperlink
from docxray.oxml.text.paragraph_props import CT_PPr
from docxray.oxml.text.run import CT_R
from docxray.oxml.xmlchemy import OxmlElement


class CT_P(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[CT_R | CT_Hyperlink]:
        return self.xpath("w:r | w:hyperlink")

    @cached_property
    def pPr(self) -> CT_PPr | None:
        return self.child_zero_or_one(W.P_PR, CT_PPr)
