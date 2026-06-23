from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import M
from docxray.oxml.trans.st.enums import SE_JC_OMATH
from docxray.oxml.trans.st.shared_math import ST_Jc
from docxray.oxml.trans.xmlchemy import OxmlElement

from .omath_elm import CT_D, CT_Acc, CT_Bar, CT_BorderBox, CT_Box, CT_EqArr

type OMathElements = CT_Acc | CT_Bar | CT_Box | CT_BorderBox | CT_D | CT_EqArr


class CT_OMathJc(OxmlElement):
    @cached_property
    def val(self) -> SE_JC_OMATH | None:
        return self.attr_optional(M.VAL, ST_Jc)


class CT_OMathParaPr(OxmlElement):
    @cached_property
    def jc(self) -> CT_OMathJc | None:
        return self.child_zero_or_one(M.JC, CT_OMathJc)


class CT_OMath(OxmlElement):
    @cached_property
    def inner_content_items(
        self,
    ) -> list[OMathElements]:
        return self.xpath(
            "m:acc | m:bar | m:box | m:borderBox | m:d | m:eqArr"
        )


class CT_OMathPara(OxmlElement):
    @cached_property
    def oMathParaPr(self) -> CT_OMathParaPr | None:
        return self.child_zero_or_one(M.O_MATH_PARA_PR, CT_OMathParaPr)

    @cached_property
    def inner_content_items(self) -> list[CT_OMath]:
        return self.child_zero_or_more(M.O_MATH, CT_OMath)
