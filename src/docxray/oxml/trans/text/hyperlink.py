from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.text.run import CT_R
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_Hyperlink(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[CT_R]:
        return self.child_zero_or_more(W.R, CT_R)
