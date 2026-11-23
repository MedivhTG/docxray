from functools import cached_property

# docxray stuff
from docxray2.ns import MEDIA_TYPE, RELATIONSHIP_TYPE
from docxray2.opc.pkg_uri import PkgURI
from docxray2.oxml.shared_dpc import E_Properties
from docxray2.proxy.custom_props import CustomProperties

from .base import DocxXmlPart


class CustomFilePropertiesPart(DocxXmlPart[E_Properties]):
    ELEMENT = E_Properties
    PART_NAME_DEFAULT = PkgURI("/docProps/custom.xml")
    CONTENT_TYPE_DEFAULT = MEDIA_TYPE.CUSTOM_PROPERTIES
    RELATIONSHIP_TYPE_DEFAULT = RELATIONSHIP_TYPE.CUSTOM_PROPERTIES

    @cached_property
    def custom_props(self) -> CustomProperties:
        return CustomProperties(self.element, self)
