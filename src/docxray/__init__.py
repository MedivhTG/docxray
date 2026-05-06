"""Initialize `docx` package.

Export the `Document` constructor function and establish the mapping of part-type to
the part-classe that implements that type.
"""

from __future__ import annotations

# docxray stuff
from docxray.api import Document

__version__ = "0.1.0"


__all__ = ["Document"]
