from typing import Any

# docxray stuff
from docxray.oxml.table.table import CT_Tbl
from docxray.resolver.resolver import BaseResolver
from docxray.shared import PropertyPath


class TableResolver(BaseResolver[CT_Tbl]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
