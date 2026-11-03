from .ns import MEDIA_TYPE
from .package import DocxPackage
from .part_factory import DocxPartFactory
from .proxy.document import Document as DocumentObject
from .types import PkgFile


def Document(docx: PkgFile) -> DocumentObject:
    package = DocxPackage.open(docx, DocxPartFactory)
    document_part = package.main_document_part
    if document_part.content_type != MEDIA_TYPE.MAIN_DOCUMENT_PART:
        raise ValueError(
            f"Media type mismatch for Word file `{docx}`: {document_part.content_type}"
        )
    return document_part.document
