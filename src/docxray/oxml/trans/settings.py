from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import CT_Language
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_Settings(OxmlElement):
    @cached_property
    def themeFontLang(self) -> CT_Language | None:
        return self.child_zero_or_one(W.THEME_FONT_LANG, CT_Language)
