from typing import Any

# docxray stuff
from docxray.oxml.table import CT_Tbl
from docxray.resolver.property_path import PropertyPath
from docxray.resolver.resolver import BaseResolver


class TableResolver(BaseResolver[CT_Tbl]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
