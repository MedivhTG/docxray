from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TypeVar

# docxray stuff
from docxray.oxml.t.proxy.base import ElementProxy, NotFound, StoryChild
from docxray.oxml.t.proxy.compute import on_off
from docxray.oxml.t.proxy.text.run_content import (
    RunInnerContent,
    run_inner_content,
)
from docxray.oxml.t.st.enums import SE_JC_OMATH, SE_TOP_BOT
from docxray.oxml.t.text.omath import CT_OMath, CT_OMathPara
from docxray.oxml.t.text.omath_elm import (
    CT_Acc,
    CT_Bar,
    CT_Box,
    CT_ManualBreak,
    CT_OMathArg,
    CT_R_OMath,
    CT_Text_OMath,
    EG_OMathMathElements,
)
from docxray.oxml.t.text.run import CT_Text

OMATH_ELM = TypeVar("OMATH_ELM", bound=EG_OMathMathElements)

# TODO: Add other proxy for iteration etc.

type OMathMathElements = Accent | Bar | BoxObject | RunOMath
type RunOMathInnerContent = TxtFragmentOMath | RunInnerContent


def iter_omath_content(parent: OMath | Arg) -> Iterator[OMathMathElements]:
    for elm in parent.element.inner_content_items:
        if isinstance(elm, CT_Acc):
            yield Accent(elm, parent)
        elif isinstance(elm, CT_Bar):
            yield Bar(elm, parent)
        elif isinstance(elm, CT_Box):
            yield BoxObject(elm, parent)
        elif isinstance(elm, CT_R_OMath):
            yield RunOMath(elm, parent)


class OMathElement(ElementProxy[OMATH_ELM]):
    pass


class Arg(ElementProxy[CT_OMathArg]):
    def iter_inner_content(self) -> Iterator[OMathMathElements]:
        return iter_omath_content(self)


class Accent(OMathElement[CT_Acc]):
    @cached_property
    def char(self) -> str:
        chr = self.prop("accPr.chr.val")
        if isinstance(chr, NotFound):
            return "\u0302"
        return chr

    @cached_property
    def argument(self) -> Arg | None:
        arg = self.element.e
        if arg is None:
            return None
        return Arg(arg, self)


class Bar(OMathElement[CT_Bar]):
    @cached_property
    def position(self) -> SE_TOP_BOT:
        pos = self.prop("barPr.pos.val")
        if isinstance(pos, NotFound):
            return SE_TOP_BOT.TOP
        return pos

    @cached_property
    def argument(self) -> Arg | None:
        arg = self.element.e
        if arg is None:
            return None
        return Arg(arg, self)


class BoxObject(OMathElement[CT_Box]):
    @cached_property
    def emulate_operator(self) -> bool:
        return on_off(self.prop("boxPr.opEmu.val"), True)

    @cached_property
    def no_wrap(self) -> bool:
        return on_off(self.prop("boxPr.noBreak.val"), True)

    @cached_property
    def as_differential(self) -> bool:
        return on_off(self.prop("boxPr.diff.val"), True)

    @cached_property
    def align_break_at(self) -> int | None:
        brk_elm: CT_ManualBreak | NotFound = self.prop("boxPr.brk")
        if isinstance(brk_elm, NotFound):
            return None
        aln = brk_elm.alnAt
        if aln is None:
            return 1
        return aln

    @cached_property
    def as_inline_block(self) -> bool:
        return on_off(self.prop("boxPr.aln.val"), True)

    @cached_property
    def argument(self) -> Arg | None:
        arg = self.element.e
        if arg is None:
            return None
        return Arg(arg, self)


class TxtFragmentOMath(ElementProxy[CT_Text_OMath]):
    @cached_property
    def raw(self) -> str:
        """Text inside of txt tag `as-is`."""
        return self._element.txt

    @cached_property
    def preserve(self) -> bool:
        """Preserve space chars inside of txt tag or not."""
        return self.element.space == "preserve"


class RunOMath(OMathElement[CT_R_OMath]):
    def iter_inner_content(self) -> Iterator[RunOMathInnerContent]:
        for item in self.element.inner_content_items:
            if isinstance(item, CT_Text_OMath):
                yield TxtFragmentOMath(item, self)
            else:
                proxy = run_inner_content(item, self)
                if proxy:
                    yield proxy


class OMath(StoryChild[CT_OMath]):
    @cached_property
    def raw_text(self) -> str:
        txt = ""
        txt_elms: list[CT_Text_OMath | CT_Text] = self.element.xpath(
            ".//m:t | .//w:t"
        )
        for txt_elm in txt_elms:
            txt += txt_elm.txt
        return txt

    def iter_inner_content(self) -> Iterator[OMathMathElements]:
        return iter_omath_content(self)


class OMathParagraph(StoryChild[CT_OMathPara]):
    @cached_property
    def alignment(self) -> SE_JC_OMATH:
        algn = self.prop("oMathParaPr.jc.val")
        if isinstance(algn, NotFound):
            return SE_JC_OMATH.CENTER_GROUP
        return algn

    @cached_property
    def raw_text(self) -> str:
        txt = ""
        txt_elms: list[CT_Text_OMath | CT_Text] = self.element.xpath(
            ".//m:t | .//w:t"
        )
        for txt_elm in txt_elms:
            txt += txt_elm.txt
        return txt

    def iter_inner_content(self) -> Iterator[OMath]:
        for item in self.element.inner_content_items:
            yield OMath(item, self)
