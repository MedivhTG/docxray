from functools import cached_property

# docxray stuff
from docxray.oxml.trans.proxy.resolvers.run import RunResolver
from docxray.oxml.trans.proxy.shared import StoryChild
from docxray.oxml.trans.text.run import CT_R


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
