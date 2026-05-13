from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import StoryChild
from docxray.oxml.trans.proxy.text.hyperlink import Hyperlink
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.text.hyperlink import CT_Hyperlink
from docxray.oxml.trans.text.paragraph import CT_P
from docxray.oxml.trans.text.run import CT_R

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.paragraph import (
        ParagraphH2D,
    )
    from docxray.oxml.trans.proxy.document import Body
    from docxray.oxml.trans.proxy.table import Cell


class Paragraph(StoryChild[CT_P]):
    @cached_property
    def h2d(self) -> ParagraphH2D:
        # docxray stuff
        from docxray.oxml.trans.h2d.paragraph import ParagraphH2D

        return ParagraphH2D(self, self.part.document_part, "pPr")

    @cached_property
    def container(self) -> Body | Cell:
        return cast("Body | Cell", self._parent)

    def iter_inner_content(self) -> Iterator[Run | Hyperlink]:
        """Generate the runs and hyperlinks in this paragraph, in the order they appear.

        The content in a paragraph consists of both runs and hyperlinks. This method
        allows accessing each of those separately, in document order, for when the
        precise position of the hyperlink within the paragraph text is important. Note
        that a hyperlink itself contains runs.
        """
        for run_or_hyperlink in self.element.inner_content_elements:
            if isinstance(run_or_hyperlink, CT_R):
                yield Run(run_or_hyperlink, self)
            elif isinstance(run_or_hyperlink, CT_Hyperlink):
                yield Hyperlink(run_or_hyperlink, self)
