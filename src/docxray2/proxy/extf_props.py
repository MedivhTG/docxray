from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.shared_dpe import E_Properties

from .base import DocxElementProxy

if TYPE_CHECKING:

    # docxray stuff
    from docxray2.parts.extended_file_properties import (  # noqa: F401
        ExtendedFilePropertiesPart,
    )


class ExtentedFileProperties(
    DocxElementProxy[E_Properties, "ExtendedFilePropertiesPart"]
):
    pass
