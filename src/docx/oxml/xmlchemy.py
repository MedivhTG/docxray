from enum import Enum
from typing import TypeVar

from docx.lxml import BaseOxmlElement

ENUM_T = TypeVar("ENUM_T", bound=Enum)


class OxmlElement(BaseOxmlElement):
    def get_enum(self, qn: str, to: type[ENUM_T]) -> ENUM_T | None:
        val = self.get(qn)
        if val is None:
            return None
        return to(val)
