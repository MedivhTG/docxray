from collections.abc import Iterator
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.text.run import CT_R
from docxray.shared import ElementProxy
from docxray.text.hyperlink import Hyperlink
from docxray.text.run import Run

if TYPE_CHECKING:
    # docxray stuff
    from docxray.blkcntnr import BlockItemContainer  # noqa: F401


class Paragraph(ElementProxy[CT_P, "BlockItemContainer"]):
    def iter_inner_content(self) -> Iterator[Run | Hyperlink]:
        """Generate the runs and hyperlinks in this paragraph, in the order they appear.

        The content in a paragraph consists of both runs and hyperlinks. This method
        allows accessing each of those separately, in document order, for when the
        precise position of the hyperlink within the paragraph text is important. Note
        that a hyperlink itself contains runs.
        """
        for run_or_hyperlink in self.element.inner_content_elements:
            yield (
                Run(run_or_hyperlink, self)
                if isinstance(run_or_hyperlink, CT_R)
                else Hyperlink(run_or_hyperlink, self)
            )
