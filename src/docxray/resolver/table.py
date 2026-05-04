from typing import Any

# docxray stuff
from docxray.oxml.table.table import CT_Row, CT_Tbl, CT_Tc
from docxray.resolver.resolver import BaseResolver
from docxray.shared import PropertyPath


class TableResolver(BaseResolver[CT_Tbl]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class RowResolver(BaseResolver[CT_Row]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None


class CellResolver(BaseResolver[CT_Tc]):
    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        return None
