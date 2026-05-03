from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.text.paragraph import CT_P
from docxray.oxml.text.run import CT_R
from docxray.resolver.property_path import PropertyPath
from docxray.resolver.resolver import BaseResolver


class RunResolver(BaseResolver[CT_R]):
    @cached_property
    def italic(self) -> bool:
        return self._prop_toggled("i")

    def _prop_toggled(self, name: str) -> bool:
        return bool(self._prop(name, is_toggled=True))

    def _from_styles_hierarchy(
        self, property_path: PropertyPath, **kwargs: Any
    ) -> Any | None:
        is_toggled = kwargs.pop("is_toggled", False)
        if is_toggled:
            return self._from_styles_toggled(property_path)
        return self._from_styles_default(property_path)

    def _from_styles_toggled(self, property_path: PropertyPath) -> bool:
        doc_path = property_path.join_left("rPrDefault")
        doc_val = self._from_doc_dflts(doc_path)
        if doc_val:
            return True
        char_val = bool(self._from_char_style(self._story_elm, property_path))
        p_elm = self._elm_ancestor(self._story_elm, CT_P)
        para_val = bool(self._from_para_style(p_elm, property_path))
        # XOR of toggled properties
        return para_val ^ char_val

    def _from_styles_default(self, property_path: PropertyPath) -> Any | None:
        return None
