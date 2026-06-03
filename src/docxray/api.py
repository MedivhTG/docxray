"""Main class for loading DOCX (Word documents)."""

from .opc.constants import CONTENT_TYPE as CT
from .oxml import TransitionalPartFactory
from .oxml.trans.package import TransitionalPackage
from .oxml.trans.proxy.document import Document as DocumentObject
from .types import PkgFile


def Document(docx: PkgFile) -> DocumentObject:
    """Load Word document of an `.docx` format (OOXML) only for reading.

    Args:
        docx (PkgFile): String path or `Path` instance or byte stream.

    Raises:
        ValueError: If cannot get document part or parse file.

    Returns:
        DocumentObject: `Document` instance.
    """
    document_part = TransitionalPackage.open(
        docx, TransitionalPartFactory
    ).main_document_part
    if document_part.content_type != CT.WML_DOCUMENT_MAIN:
        tmpl = "file '%s' is not a Word file, content type is '%s'"
        raise ValueError(tmpl % (docx, document_part.content_type))
    return document_part.document
