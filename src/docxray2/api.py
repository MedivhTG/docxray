from .ns import MEDIA_TYPE
from .oxml.proxy.document import Document as DocumentObject
from .package import DocxPackage
from .part_factory import DocxPartFactory
from .types import PkgFile


def Document(file: PkgFile) -> DocumentObject:
    package = DocxPackage.open(file, DocxPartFactory)
    document_part = package.main_document_part
    if document_part.content_type != MEDIA_TYPE.MAIN_DOCUMENT:
        raise ValueError(
            f"Media type mismatch for Word file `{file}`: {document_part.content_type}"
        )
    return document_part.document
