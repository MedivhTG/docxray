from functools import cached_property

# docxray stuff
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.xmlchemy import OxmlElement


class CT_Tbl(OxmlElement):
    pass


class CT_Tc(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        return self.xpath("w:p | w:tbl")
