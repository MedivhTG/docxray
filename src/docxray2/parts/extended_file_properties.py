from functools import cached_property

# docxray stuff
from docxray2.ns import MEDIA_TYPE, NAMESPACE, RELATIONSHIP_TYPE
from docxray2.opc.pkg_uri import PkgURI
from docxray2.oxml.shared_dpe import E_Properties
from docxray2.proxy.extf_props import ExtentedFileProperties

from .base import DocxXmlPart


class ExtendedFilePropertiesPart(DocxXmlPart[E_Properties]):
    ELEMENT = E_Properties
    PART_NAME_DEFAULT = PkgURI("/docProps/app.xml")
    CONTENT_TYPE_DEFAULT = MEDIA_TYPE.EXTENDED_FILE_PROPERTIES
    RELATIONSHIP_TYPE_DEFAULT = RELATIONSHIP_TYPE.EXTENDED_PROPERTIES
    NSMAP_DEFAULT = {
        None: NAMESPACE.EXTENDED_PROPERTIES,
        "vt": NAMESPACE.VARIANT_TYPES,
    }

    @cached_property
    def extf_props(self) -> ExtentedFileProperties:
        return ExtentedFileProperties(self.element, self)
