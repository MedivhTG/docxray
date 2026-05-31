from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing
from docxray.oxml.trans.ns import XML, W
from docxray.oxml.trans.shared import CT_Empty
from docxray.oxml.trans.st.enums import SE_BR_CLEAR, SE_BR_TYPE
from docxray.oxml.trans.st.shared_common import ST_String
from docxray.oxml.trans.st.wml import ST_BrClear, ST_BrType, ST_ShortHexNumber
from docxray.oxml.trans.text.run_props import CT_RPr
from docxray.oxml.trans.xmlchemy import OxmlElement


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


class CT_Text(OxmlElement):
    @cached_property
    def txt(self) -> str:
        return self.text or ""

    @cached_property
    def space(self) -> str | None:
        return self.attr_optional(XML.SPACE, ST_String)


class CT_Br(OxmlElement):
    @cached_property
    def type(self) -> SE_BR_TYPE | None:
        return self.attr_optional(W.TYPE, ST_BrType)

    @cached_property
    def clear_attr(self) -> SE_BR_CLEAR | None:
        return self.attr_optional(W.CLEAR, ST_BrClear)


class CT_Sym(OxmlElement):
    @cached_property
    def font(self) -> str | None:
        return self.attr_optional(W.FONT, ST_String)

    @cached_property
    def char(self) -> bytes | None:
        return self.attr_optional(W.CHAR, ST_ShortHexNumber)


class CT_PTab(OxmlElement):
    pass


type RunInnerContent = list[CT_Br | CT_Text | CT_Empty | CT_Drawing | CT_PTab]


class CT_R(OxmlElement):
    @cached_property
    def t(self) -> CT_Text | None:
        return self.child_zero_or_one(W.T, CT_Text)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def inner_content_items(self) -> RunInnerContent:
        xpath = (
            "w:br | w:t | w:noBreakHyphen | w:softHyphen | w:sym | w:cr | w:tab | "
            "w:drawing | w:ptab"
        )
        return self.xpath(xpath)
