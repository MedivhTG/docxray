"""Exceptions used with python-docx.

The base exception class is PythonDocxError.
"""


class DocxrayError(Exception):
    """Generic error class."""


class InvalidSpanError(DocxrayError):
    """Raised when an invalid merge region is specified in a request to merge table
    cells."""


class InvalidXmlError(DocxrayError):
    """Raised when invalid XML is encountered, such as on attempt to access a missing
    required child element."""
