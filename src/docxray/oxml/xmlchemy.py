from enum import Enum
from typing import TypeVar

from lxml.etree import LxmlError

# docxray stuff
from docxray.lxml import BaseOxmlElement
from docxray.types import ELM_T

ENUM_T = TypeVar("ENUM_T", bound=Enum)


class OxmlError(LxmlError):
    pass


class OxmlElement(BaseOxmlElement):
    def get_enum(self, qn: str, to: type[ENUM_T]) -> ENUM_T | None:
        val = self.get(qn)
        if val is None:
            return None
        return to(val)

    def child_one(self, qn: str, elm_hint: type[ELM_T]) -> ELM_T:
        child = self.find(qn, elm_hint)
        if child is None:
            msg = f"Cannot get child '{qn}' from {self}"
            raise OxmlError(msg)
        return child
