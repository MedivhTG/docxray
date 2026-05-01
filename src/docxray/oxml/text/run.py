from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.text.run_props import CT_RPr
from docxray.oxml.xmlchemy import OxmlElement


class CT_T(OxmlElement):
    @cached_property
    def txt(self) -> str:
        return self.text or ""


class CT_R(OxmlElement):
    @cached_property
    def t(self) -> CT_T | None:
        return self.child_zero_or_first(W.T, CT_T)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_first(W.R_PR, CT_RPr)

    @cached_property
    def inner_content_items(self) -> list[CT_T]:
        return self.xpath("w:t")
