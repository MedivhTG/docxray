from typing import Any

# docxray stuff
from docxray.format.format import BaseFormat
from docxray.format.property_path import PropertyPath
from docxray.oxml.table import CT_Tbl


class TableFormat(BaseFormat[CT_Tbl]):
    def _rslv_from_styles(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
