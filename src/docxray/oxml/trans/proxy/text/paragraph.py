from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.enums import WD_HEADER_LEVEL
from docxray.oxml.trans.proxy.shared import Length, StoryChild
from docxray.oxml.trans.proxy.text.hyperlink import Hyperlink
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.st.enums import SE_JC
from docxray.oxml.trans.text.hyperlink import CT_Hyperlink
from docxray.oxml.trans.text.paragraph import CT_P
from docxray.oxml.trans.text.run import CT_R
from docxray.transform.paragraph import ParagraphT
from docxray.transform.ruleset import RuleSet

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.h2d.paragraph import (
        ListItem,
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

    @cached_property
    def list_item(self) -> ListItem | None:
        return self.h2d.list_item

    @cached_property
    def right_to_left(self) -> bool:
        return self.h2d.right_to_left

    @cached_property
    def text_indent(self) -> Length | int | None:
        return self.h2d.text_indent

    @cached_property
    def header_level(self) -> WD_HEADER_LEVEL:
        return self.h2d.header_level

    @cached_property
    def alignment(self) -> SE_JC:
        return self.h2d.alignment

    @cached_property
    def word_wrap(self) -> bool:
        return self.h2d.word_wrap

    @cached_property
    def justify_inter_character(self) -> bool:
        return self.h2d.justify_inter_character

    def transform(self, ruleset: RuleSet | None = None) -> str:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return ParagraphT.transform(self, ruleset)

    # TODO: not all but enough
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
