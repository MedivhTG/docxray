from functools import cached_property

# docxray stuff
from docxray.oxml.t.part import TransitionalPart
from docxray.oxml.t.proxy.settings import Settings
from docxray.oxml.t.settings import CT_Settings


class SettingsPart(TransitionalPart[CT_Settings]):
    @cached_property
    def settings(self) -> Settings:
        return Settings(self.element, self)
