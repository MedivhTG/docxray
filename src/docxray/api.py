"""Directly exposed API functions and classes, :func:`Document` for now.

Provides a syntactically more convenient API for interacting with the OpcPackage graph.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray.opc.constants import CONTENT_TYPE as CT
from docxray.package import Package
from docxray.types import PkgFile

if TYPE_CHECKING:
    # docxray stuff
    from docxray.proxy.document import Document as DocumentObject


def Document(docx: PkgFile) -> DocumentObject:
    """Return a |Document| object loaded from `docx`, where `docx` can be either a path
    to a ``.docx`` file (a string) or a file-like object.

    If `docx` is missing or ``None``, the built-in default document "template" is
    loaded.
    """
    document_part = Package.open(docx).main_document_part
    if document_part.content_type != CT.WML_DOCUMENT_MAIN:
        tmpl = "file '%s' is not a Word file, content type is '%s'"
        raise ValueError(tmpl % (docx, document_part.content_type))
    return document_part.document
