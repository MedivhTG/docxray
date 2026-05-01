from functools import cached_property
from typing import Any

# docxray stuff
from docxray.format.format import BaseFormat
from docxray.format.property_path import PropertyPath
from docxray.oxml.text.run import CT_R


class RunFormat(BaseFormat[CT_R]):
    @cached_property
    def italic(self) -> bool:
        return self._rslv_prop_toggled("i")

    def _rslv_prop_toggled(self, name: str) -> bool:
        return bool(self._rslv_prop(name, is_toggled=True))

    def _rslv_from_styles(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        is_toggled = kwargs.pop("is_toggled", False)
        if is_toggled:
            return self._rslv_from_styles_toggled(property_path)
        return self._rslv_from_styles_default(property_path)

    def _rslv_from_styles_toggled(self, property_path: PropertyPath) -> bool:
        doc_path = property_path.join_left("rPrDefault")
        val = self._rslv_from_doc_dflts(doc_path)
        if val:
            return True
        return False

    def _rslv_from_styles_default(
        self, propety_path: PropertyPath
    ) -> Any | None:
        return None
