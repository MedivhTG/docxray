from functools import cached_property

# docxray stuff
from docxray.oxml.trans.part import TransitionalPart
from docxray.oxml.trans.proxy.settings import Settings
from docxray.oxml.trans.settings import CT_Settings


class SettingsPart(TransitionalPart[CT_Settings]):
    @cached_property
    def settings(self) -> Settings:
        return Settings(self.element, self)
