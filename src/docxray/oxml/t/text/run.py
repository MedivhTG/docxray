from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.t.drawing import CT_Drawing
from docxray.oxml.t.ns import XML, W
from docxray.oxml.t.shared import CT_Empty, CT_Markup, CT_Rel
from docxray.oxml.t.st.enums import SE_BR_CLEAR, SE_BR_TYPE
from docxray.oxml.t.st.shared_common import ST_String
from docxray.oxml.t.st.wml import (
    ST_BrClear,
    ST_BrType,
    ST_LongHexNumber,
    ST_ShortHexNumber,
)
from docxray.oxml.t.xmlchemy import OxmlElement

from .run_props import CT_RPr

type EG_RunInnerContent = CT_Br | CT_Text | CT_Rel | CT_Empty | CT_Sym | CT_Object | CT_Picture_RUN | CT_FldChar | CT_Ruby | CT_FtnEdnRef | CT_Markup | CT_Drawing | CT_PTab
XPATH_RUN_INNER_CONTENT = "w:br | w:t | w:noBreakHyphen | w:softHyphen | w:sym | w:cr | w:tab | w:drawing | w:ptab"


class CT_Object(OxmlElement):
    pass


class CT_RunTrackChange(OxmlElement):
    pass


class CT_SdtRun(OxmlElement):
    pass


class CT_DirContentRun(OxmlElement):
    pass


class CT_BdoContentRun(OxmlElement):
    pass


class CT_SmartTagRun(OxmlElement):
    pass


class CT_CustomXmlRun(OxmlElement):
    pass


class CT_Picture_RUN(OxmlElement):
    pass


class CT_FldChar(OxmlElement):
    pass


class CT_Ruby(OxmlElement):
    pass


class CT_FtnEdnRef(OxmlElement):
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


class CT_R(OxmlElement):
    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def inner_content_items(self) -> list[EG_RunInnerContent]:
        return self.xpath(XPATH_RUN_INNER_CONTENT)

    @cached_property
    def rsidRPr(self) -> bytes | None:
        return self.attr_optional(W.RSID_R_PR, ST_LongHexNumber)

    @cached_property
    def rsidDel(self) -> bytes | None:
        return self.attr_optional(W.RSID_DEL, ST_LongHexNumber)

    @cached_property
    def rsidR(self) -> bytes | None:
        return self.attr_optional(W.RSID_R, ST_LongHexNumber)
