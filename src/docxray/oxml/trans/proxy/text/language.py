from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.base import ElementProxy
from docxray.oxml.trans.shared import CT_Language


class Language(ElementProxy[CT_Language]):
    @cached_property
    def latin_slot(self) -> str | None:
        return self.element.val

    @cached_property
    def east_asia_slot(self) -> str | None:
        return self.element.eastAsia

    @cached_property
    def complex_script_slot(self) -> str | None:
        return self.element.bidi
