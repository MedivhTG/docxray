from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.trans.proxy.shared import StoryChild
from docxray.oxml.trans.text.run import CT_R

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.resolvers.run import RunResolver


class Run(StoryChild[CT_R]):
    @cached_property
    def resolver(self) -> RunResolver:
        # docxray stuff
        from docxray.oxml.trans.proxy.resolvers.run import RunResolver

        return RunResolver(self, self.part.document_part, "rPr")

    @cached_property
    def raw_text(self) -> str:
        t_elm = self.element.t
        if t_elm is None:
            return ""
        return t_elm.txt
