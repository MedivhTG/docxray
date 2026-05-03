from functools import cached_property

# docxray stuff
from docxray.enum.table import WD_CNF_FORMAT
from docxray.oxml.ns import W
from docxray.oxml.simpletypes import ST_Cnf
from docxray.oxml.xmlchemy import OxmlElement


class CT_Cnf(OxmlElement):
    @cached_property
    def val(self) -> WD_CNF_FORMAT:
        return ST_Cnf.validate(self.get(W.VAL))
