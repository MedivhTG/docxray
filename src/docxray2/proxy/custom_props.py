from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.shared_dpc import E_Properties

from .base import DocxElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.parts.custom_file_properties import (  # noqa: F401
        CustomFilePropertiesPart,
    )


class CustomProperties(
    DocxElementProxy[E_Properties, "CustomFilePropertiesPart"]
):
    pass
