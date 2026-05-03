from typing import Any

# docxray stuff
from docxray.oxml.text.paragraph import CT_P
from docxray.resolver.resolver import BaseResolver
from docxray.shared import PropertyPath


class ParagraphResolver(BaseResolver[CT_P]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
