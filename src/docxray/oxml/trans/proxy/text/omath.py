from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    StoryChild,
    safe_get_prop,
)
from docxray.oxml.trans.st.enums import SE_JC_OMATH
from docxray.oxml.trans.text.omath import CT_OMath, CT_OMathPara


class OMath(StoryChild[CT_OMath]):
    @cached_property
    def raw_text(self) -> str:
        return ""


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
        return ""
