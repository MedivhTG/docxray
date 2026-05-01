from functools import cached_property

# docxray stuff
from docxray.format.run import RunFormat
from docxray.oxml.text.run import CT_R
from docxray.shared import StoryChild


class Run(StoryChild[CT_R]):
    @cached_property
    def fmt(self) -> RunFormat:
        return RunFormat(self.element, self.part.document_part)

    @cached_property
    def raw_text(self) -> str:
        t_elm = self.element.t
        if t_elm is None:
            return ""
        return t_elm.txt
