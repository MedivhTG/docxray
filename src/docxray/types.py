"""Abstract types used by `python-docx`."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO, TypeVar

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.xmlchemy import OxmlElement

ELM_T = TypeVar("ELM_T", bound="OxmlElement")

type PkgFile = str | Path | BinaryIO
