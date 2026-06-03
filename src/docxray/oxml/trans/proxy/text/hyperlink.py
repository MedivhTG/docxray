from __future__ import annotations

from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, cast

# docxray stuff
from docxray.oxml.trans.proxy.shared import ElementProxy
from docxray.oxml.trans.proxy.text.run import Run
from docxray.oxml.trans.text.hyperlink import CT_Hyperlink
from docxray.oxml.trans.text.run import CT_R

if TYPE_CHECKING:
    from .paragraph import Paragraph


class Hyperlink(ElementProxy[CT_Hyperlink]):
    @cached_property
    def paragraph(self) -> Paragraph:
        return cast("Paragraph", self._parent)

    def iter_inner_content(self) -> Iterator[Run]:
        for run_or_hyperlink in self.element.inner_content_elements:
            if isinstance(run_or_hyperlink, CT_R):
                yield Run(run_or_hyperlink, self)  # type: ignore[arg-type]
