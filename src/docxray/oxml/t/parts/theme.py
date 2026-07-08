from functools import cached_property

# docxray stuff
from docxray.oxml.t.part import TransitionalPart
from docxray.oxml.t.proxy.theme import Theme
from docxray.oxml.t.theme.theme import CT_OfficeStyleSheet


class ThemePart(TransitionalPart[CT_OfficeStyleSheet]):
    @cached_property
    def theme(self) -> Theme:
        return Theme(self.element, self)
