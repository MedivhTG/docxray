from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.t.ns import W
from docxray.oxml.t.shared import (
    CT_Markup,
    CT_Perm,
    CT_PermStart,
    CT_ProofErr,
    CT_Rel,
    CT_TrackChange,
)
from docxray.oxml.t.st.wml import ST_LongHexNumber
from docxray.oxml.t.xmlchemy import OxmlElement

from .hyperlink import CT_Hyperlink
from .omath import CT_OMath, CT_OMathPara
from .paragraph_props import CT_PPr
from .range import CT_Bookmark, CT_MarkupRange, CT_MoveBookmark
from .run import (
    CT_R,
    CT_BdoContentRun,
    CT_CustomXmlRun,
    CT_DirContentRun,
    CT_RunTrackChange,
    CT_SdtRun,
    CT_SmartTagRun,
)

type EG_MathContent = CT_OMathPara | CT_OMath
type EG_RangeMarkupElements = CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup
type EG_RunLevelElts = CT_ProofErr | CT_PermStart | CT_Perm | EG_RangeMarkupElements | CT_RunTrackChange | EG_MathContent
type EG_ContentRunContent = CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | EG_RunLevelElts
type EG_PContent = EG_ContentRunContent | CT_SimpleField | CT_Hyperlink | CT_Rel

_XPATH_OMATH = "m:oMathPara | m:oMath"
_XPATH_RANGE_MARKUP = (
    "w:bookmarkStart | "
    "w:bookmarkEnd | w:moveFromRangeStart | w:moveFromRangeEnd | "
    "w:moveToRangeStart | w:commentRangeEnd | w:customXmlInsRangeStart | "
    "w:customXmlInsRangeEnd | w:customXmlDelRangeStart | "
    "w:customXmlDelRangeEnd | w:customXmlMoveFromRangeStart | "
    "w:customXmlMoveFromRangeEnd | w:customXmlMoveToRangeStart | "
    "w:customXmlMoveToRangeEnd "
)
_XPATH_RUN_LEVEL_ELTS = (
    f"w:proofErr | w:permStart | w:permEnd | w:bookmarkStart | {_XPATH_RANGE_MARKUP} | "
    f"w:ins | w:del | w:moveFrom | w:moveTo | {_XPATH_OMATH}"
)
_XPATH_RUN_CONTENT = f"w:customXml | w:smartTag | w:sdt | w:dir | w:bdo | w:r | {_XPATH_RUN_LEVEL_ELTS}"
XPATH_P_CONTENT = (
    f"{_XPATH_RUN_CONTENT} | w:fldSimple | w:hyperlink | w:subDoc"
)


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
    def inner_content_elements(self) -> list[EG_PContent]:
        return self.xpath(XPATH_P_CONTENT)
