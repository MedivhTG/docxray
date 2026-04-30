"""|Document| and closely related objects."""

from docx.oxml.document import CT_Document
from docx.shared import ElementProxy


class Document(ElementProxy[CT_Document]):
    """WordprocessingML (WML) document.

    Not intended to be constructed directly. Use :func:`docx.Document` to open or create
    a document.
    """
