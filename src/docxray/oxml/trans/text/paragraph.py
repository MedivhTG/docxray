from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.st.wml import ST_LongHexNumber
from docxray.oxml.trans.text.hyperlink import CT_Hyperlink
from docxray.oxml.trans.text.paragraph_props import CT_PPr
from docxray.oxml.trans.text.run import CT_R
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_Rel(OxmlElement):
    pass


class CT_SimpleField(OxmlElement):
    pass


class CT_P(OxmlElement):
    @cached_property
    def rsidRPr(self) -> bytes | None:
        return self.attr_optional(W.RSID_R_PR, ST_LongHexNumber)

    @cached_property
    def rsidR(self) -> bytes | None:
        return self.attr_optional(W.RSID_R, ST_LongHexNumber)

    @cached_property
    def rsidDel(self) -> bytes | None:
        return self.attr_optional(W.RSID_DEL, ST_LongHexNumber)

    @cached_property
    def rsidP(self) -> bytes | None:
        return self.attr_optional(W.RSID_P, ST_LongHexNumber)

    @cached_property
    def rsidRDefault(self) -> bytes | None:
        return self.attr_optional(W.RSID_R_DEFAULT, ST_LongHexNumber)

    @cached_property
    def pPr(self) -> CT_PPr | None:
        return self.child_zero_or_one(W.P_PR, CT_PPr)

    @cached_property
    def inner_content_elements(self) -> list[CT_R | CT_Hyperlink]:
        return self.xpath("w:r | w:hyperlink")
