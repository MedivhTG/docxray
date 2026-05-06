from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.text.run import CT_R
from docxray.resolver.run import RunResolver
from docxray.shared import StoryChild


class Run(StoryChild[CT_R]):
    @cached_property
    def resolver(self) -> RunResolver:
        return RunResolver(self.element, self.part.document_part, "rPr")

    @cached_property
    def raw_text(self) -> str:
        t_elm = self.element.t
        if t_elm is None:
            return ""
        return t_elm.txt
