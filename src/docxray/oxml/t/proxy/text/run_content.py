from enum import StrEnum
from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.t.drawing import CT_Drawing
from docxray.oxml.t.ns import W
from docxray.oxml.t.proxy.base import ElementProxy
from docxray.oxml.t.proxy.drawing import Drawing
from docxray.oxml.t.proxy.vml import VMLObject
from docxray.oxml.t.shared import CT_Empty, CT_Markup, CT_Rel
from docxray.oxml.t.st.enums import SE_BR_CLEAR, SE_BR_TYPE
from docxray.oxml.t.text.run import (
    CT_Br,
    CT_FldChar,
    CT_FtnEdnRef,
    CT_Object,
    CT_Picture_RUN,
    CT_PTab,
    CT_Ruby,
    CT_Sym,
    CT_Text,
    EG_RunInnerContent,
)

type RunInnerContent = (
    TxtFragment
    | Drawing
    | Break
    | Tab
    | AbsolutePositionTab
    | NonBreakHyphen
    | OptionalHyphen
    | CarriageReturn
    | Symbol
    | ComplexField
    | PageNumber
    | DateBlock
    | FootnoteReference
    | FootnoteMark
    | Comment
    | Separator
    | ContinuationSeparatorMark
    | PhoneticGuide
    | ContentPart
    | LastCalculatedPageBreak
    | VMLObject
    | EmbeddedObject
)
_DATE_BLOCKS = {
    W.DAY_SHORT,
    W.MONTH_SHORT,
    W.YEAR_SHORT,
    W.DAY_LONG,
    W.MONTH_LONG,
    W.YEAR_LONG,
}
_FOOTNOTE_MARKS = {W.FOOTNOTE_REF, W.ENDNOTE_REF, W.ANNOTATION_REF}


def run_inner_content(
    item: EG_RunInnerContent, instance: Any
) -> RunInnerContent:
    if isinstance(item, CT_Text):
        return TxtFragment(item, instance)
    elif isinstance(item, CT_Drawing):
        return Drawing(item, instance)
    elif isinstance(item, CT_Br):
        return Break(item, instance)
    elif isinstance(item, CT_FtnEdnRef):
        return FootnoteReference(item, instance)
    elif isinstance(item, CT_Empty):
        if item.tag == W.TAB:
            return Tab(item, instance)
        elif item.tag == W.LAST_RENDERED_PAGE_BREAK:
            return LastCalculatedPageBreak(item, instance)
        elif item.tag in _FOOTNOTE_MARKS:
            return FootnoteMark(item, instance)
        elif item.tag == W.NO_BREAK_HYPHEN:
            return NonBreakHyphen(item, instance)
        elif item.tag == W.SOFT_HYPHEN:
            return OptionalHyphen(item, instance)
        elif item.tag == W.CR:
            return CarriageReturn(item, instance)
        elif item.tag == W.PG_NUM:
            return PageNumber(item, instance)
        elif item.tag == W.SEPARATOR:
            return Separator(item, instance)
        elif item.tag == W.CONTINUATION_SEPARATOR:
            return ContinuationSeparatorMark(item, instance)
        elif item.tag in _DATE_BLOCKS:
            return DateBlock(item, instance)
    elif isinstance(item, CT_Picture_RUN):
        return VMLObject(item, instance)
    elif isinstance(item, CT_Object):
        return EmbeddedObject(item, instance)
    elif isinstance(item, CT_Sym):
        return Symbol(item, instance)
    elif isinstance(item, CT_Markup):
        return Comment(item, instance)
    elif isinstance(item, CT_Rel):
        return ContentPart(item, instance)
    elif isinstance(item, CT_Ruby):
        return PhoneticGuide(item, instance)
    elif isinstance(item, CT_PTab):
        return AbsolutePositionTab(item, instance)
    elif isinstance(item, CT_FldChar):
        return ComplexField(item, instance)
    raise TypeError(f"No such type for {item} of class {item.__class__}")


class Tab(ElementProxy[CT_Empty]):
    pass


# TODO: implement?
class AbsolutePositionTab(ElementProxy[CT_PTab]):
    pass


class NonBreakHyphen(ElementProxy[CT_Empty]):
    pass


class OptionalHyphen(ElementProxy[CT_Empty]):
    pass


class CarriageReturn(ElementProxy[CT_Empty]):
    pass


class Symbol(ElementProxy[CT_Sym]):
    @cached_property
    def character(self) -> str:
        ch = self.element.char
        if ch is None:
            sym = ""
        else:
            sym = ch.hex()
        return chr(int(sym, 16))

    @cached_property
    def font(self) -> str | None:
        return self.element.font


# TODO: implement
class ComplexField(ElementProxy[CT_FldChar]):
    pass


# TODO: implement?
class PageNumber(ElementProxy[CT_Empty]):
    pass


class FOOTNOTE_MARK_TYPE(StrEnum):
    FOOTNOTE = "footnoteRef"
    ENDNOTE = "endnoteRef"
    ANNOTATION = "annotationRef"


class FootnoteMark(ElementProxy[CT_Empty]):
    @cached_property
    def mark_type(self) -> FOOTNOTE_MARK_TYPE:
        return FOOTNOTE_MARK_TYPE(self.element.tag_name)


# TODO: implement?
class Comment(ElementProxy[CT_Markup]):
    pass


# TODO: implement?
class FootnoteReference(ElementProxy[CT_FtnEdnRef]):
    pass


class Separator(ElementProxy[CT_Empty]):
    pass


# TODO: implement?
class ContinuationSeparatorMark(ElementProxy[CT_Empty]):
    pass


# TODO: implement
class ContentPart(ElementProxy[CT_Rel]):
    pass


class DATE_BLOCK_FMT(StrEnum):
    SHORT_DAY = "dayShort"
    SHORT_MONTH = "monthShort"
    SHORT_YEAR = "yearShort"
    LONG_DAY = "dayLong"
    LONG_MONTH = "monthLong"
    LONG_YEAR = "yearLong"


# TODO: implement?
class DateBlock(ElementProxy[CT_Empty]):
    @cached_property
    def format(self) -> DATE_BLOCK_FMT:
        return DATE_BLOCK_FMT(self.element.tag_name)


class Break(ElementProxy[CT_Br]):
    @cached_property
    def break_type(self) -> SE_BR_TYPE:
        if self.element.type is None:
            return SE_BR_TYPE.TEXT_WRAPPING
        return self.element.type

    @cached_property
    def how_wrap(self) -> SE_BR_CLEAR:
        if self.break_type != SE_BR_TYPE.TEXT_WRAPPING:
            return SE_BR_CLEAR.NONE
        if self.element.clear_attr is None:
            return SE_BR_CLEAR.NONE
        return self.element.clear_attr


# TODO: implement?
class PhoneticGuide(ElementProxy[CT_Ruby]):
    pass


class LastCalculatedPageBreak(ElementProxy[CT_Empty]):
    pass


# TODO: implement?
class EmbeddedObject(ElementProxy[CT_Object]):
    pass


class TXT_FGMT_TYPE(StrEnum):
    TEXT = "t"
    DELETED_TEXT = "delText"
    FIELD_CODE = "instrText"
    DELETED_FIELD_CODE = "delInstrText"


class TxtFragment(ElementProxy[CT_Text]):
    @cached_property
    def raw(self) -> str:
        """Text inside of txt tag `as-is`."""
        return self._element.txt

    @cached_property
    def preserve(self) -> bool:
        """Preserve space chars inside of txt tag or not."""
        return self.element.space == "preserve"

    @cached_property
    def txt_type(self) -> TXT_FGMT_TYPE:
        """Determines if text is common txt-container or special tag."""
        return TXT_FGMT_TYPE(self.element.tag_name)
