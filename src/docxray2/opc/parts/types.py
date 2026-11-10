from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .base import OpcXmlPart


class ProvidesOpcXmlPart(Protocol):
    @property
    def _part(self) -> OpcXmlPart: ...
