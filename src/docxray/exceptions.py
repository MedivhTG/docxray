"""Module with exception used in `docxray`."""


class DocxrayError(Exception):
    """Generic error class."""


class InvalidXmlError(DocxrayError):
    """Raised when invalid XML is encountered, such as on attempt to access a missing
    required child element."""
