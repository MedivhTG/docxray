from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, TypeVar, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import (
    ElementProxy,
    NotFound,
    PropertyPath,
    StoryChild,
    safe_get_prop,
)
from docxray.oxml.trans.st.enums import SE_JC_OMATH
from docxray.oxml.trans.text.omath import CT_OMath, CT_OMathPara
from docxray.oxml.trans.text.omath_elm import (
    CT_Acc,
    CT_OMathArg,
    CT_R_OMath,
    CT_Text_OMath,
    OMathElements,
)
from docxray.oxml.trans.text.run import CT_Text
from docxray.transform.transformer import Transformer

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet
    from docxray.transform.transformer import TransformMethod

OMATH_ELM = TypeVar("OMATH_ELM", bound=OMathElements)

# TODO: Add other proxy fo iteration etc.

type OMathElementsProxy = Accent | RunOMath
type RunOMathContent = TxtFragmentOMath


def iter_omath_content(parent: OMath | Arg) -> Iterator[OMathElementsProxy]:
    for elm in parent.element.inner_content_items:
        if isinstance(elm, CT_Acc):
            yield Accent(elm, parent)
        elif isinstance(elm, CT_R_OMath):
            yield RunOMath(elm, parent)


class OMathElement(ElementProxy[OMATH_ELM]):
    def _prop(self, path: PropertyPath, optional: bool = False) -> Any:
        return safe_get_prop(self.element, path, optional)


class Arg(ElementProxy[CT_OMathArg]):
    def iter_inner_content(self) -> Iterator[OMathElementsProxy]:
        return iter_omath_content(self)


class Accent(OMathElement[CT_Acc]):
    @cached_property
    def char(self) -> str:
        chr = self._prop(PropertyPath.base("val", "accPr.chr"))
        if isinstance(chr, NotFound):
            return "\u0302"
        return chr

    @cached_property
    def argument(self) -> Arg | None:
        arg = self.element.e
        if arg is None:
            return None
        return Arg(arg, self)


class TxtFragmentOMath(ElementProxy[CT_Text_OMath]):
    @cached_property
    def raw(self) -> str:
        return self._element.txt

    @cached_property
    def preserve(self) -> bool:
        return self.element.space == "preserve"


class RunOMath(OMathElement[CT_R_OMath]):
    def iter_inner_content(self) -> Iterator[RunOMathContent]:
        for item in self.element.inner_content_items:
            if isinstance(item, CT_Text_OMath):
                yield TxtFragmentOMath(item, self)


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

    def iter_inner_content(self) -> Iterator[OMathElementsProxy]:
        return iter_omath_content(self)

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(self, ruleset, "OMath", stringify, method)


class OMathParagraph(StoryChild[CT_OMathPara]):
    @cached_property
    def alignment(self) -> SE_JC_OMATH:
        algn = safe_get_prop(
            self.element, PropertyPath.base("val", "oMathParaPr.jc"), False
        )
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

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(
            self, ruleset, "OMathParagraph", stringify, method
        )
