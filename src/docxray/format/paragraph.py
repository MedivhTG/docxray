from typing import Any

# docxray stuff
from docxray.format.format import BaseFormat
from docxray.format.property_path import PropertyPath
from docxray.oxml.text.paragraph import CT_P


class ParagraphFormat(BaseFormat[CT_P]):
    def _rslv_from_styles(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
