from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.ns import W
from docxray.oxml.transitional.text.run_props import CT_RPr
from docxray.oxml.transitional.xmlchemy import OxmlElement


class CT_RunTrackChange(OxmlElement):
    pass


class CT_Perm(OxmlElement):
    pass


class CT_PermStart(OxmlElement):
    pass


class CT_ProofErr(OxmlElement):
    pass


class CT_SdtRun(OxmlElement):
    pass


class CT_SmartTagRun(OxmlElement):
    pass


class CT_CustomXmlRun(OxmlElement):
    pass


class CT_R(OxmlElement):
    @cached_property
    def t(self) -> CT_T | None:
        return self.child_zero_or_one(W.T, CT_T)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def inner_content_items(self) -> list[CT_T]:
        return self.xpath("w:t")


class CT_T(OxmlElement):
    @cached_property
    def txt(self) -> str:
        return self.text or ""
