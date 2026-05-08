from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.trans.proxy.shared import StoryChild
from docxray.oxml.trans.text.run import CT_R

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.proxy.h2d.run_h2d import RunH2D


class Run(StoryChild[CT_R]):
    @cached_property
    def h2d(self) -> RunH2D:
        # docxray stuff
        from docxray.oxml.trans.proxy.h2d.run_h2d import RunH2D
        from docxray.oxml.trans.proxy.h2d.run_rslv import RunResolver

        return RunH2D(RunResolver(self, self.part.document_part, "rPr"))

    @cached_property
    def raw_text(self) -> str:
        t_elm = self.element.t
        if t_elm is None:
            return ""
        return t_elm.txt
