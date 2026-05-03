from functools import cached_property

# docxray stuff
from docxray.oxml.ns import W
from docxray.oxml.xmlchemy import OxmlElement


class CT_String(OxmlElement):
    @cached_property
    def val(self) -> str:
        return self.get_attr_one(W.VAL)
