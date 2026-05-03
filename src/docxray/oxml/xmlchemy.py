from typing import Any

from lxml.etree import LxmlError

# docxray stuff
from docxray.lxml import BaseOxmlElement
from docxray.oxml.ns import nsmap
from docxray.types import ELM_T


class OxmlError(LxmlError):
    pass


class OxmlElement(BaseOxmlElement):
    def xpath(self, xpath: str) -> Any:  # type: ignore[override]
        return super().xpath(xpath, nsmap)

    def child_first_only(self, qn: str, elm_hint: type[ELM_T]) -> ELM_T:
        child = self.find(qn, elm_hint)
        if child is None:
            msg = f"Cannot get child '{qn}' from {self}"
            raise OxmlError(msg)
        return child

    def child_zero_or_first(
        self, qn: str, elm_hint: type[ELM_T]
    ) -> ELM_T | None:
        return self.find(qn, elm_hint)

    def child_zero_or_more(
        self, qn: str, elm_hint: type[ELM_T]
    ) -> list[ELM_T]:
        return self.findall(qn, elm_hint)
