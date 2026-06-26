from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    StoryChild,
    safe_get_prop,
)
from docxray.oxml.trans.st.enums import SE_JC_OMATH
from docxray.oxml.trans.text.omath import CT_OMath, CT_OMathPara
from docxray.oxml.trans.text.omath_elm import CT_Text_OMath
from docxray.oxml.trans.text.run import CT_Text
from docxray.transform.transformer import Transformer

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet
    from docxray.transform.transformer import TransformMethod


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
