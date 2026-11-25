from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.shared_cxdp import E_DatastoreItem

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.parts.custom_xml_data_properties import (  # noqa: F401
        CustomXmlDataPropertiesPart,
    )

from .base import DocxElementProxy


class CustomXml(
    DocxElementProxy[E_DatastoreItem, "CustomXmlDataPropertiesPart"]
):
    pass
