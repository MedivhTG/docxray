from functools import cached_property

# docxray stuff
from docxray.oxml.trans.part import TransitionalPart
from docxray.oxml.trans.proxy.theme import Theme
from docxray.oxml.trans.theme.theme import CT_OfficeStyleSheet


class ThemePart(TransitionalPart[CT_OfficeStyleSheet]):
    @cached_property
    def theme(self) -> Theme:
        return Theme(self.element, self)
