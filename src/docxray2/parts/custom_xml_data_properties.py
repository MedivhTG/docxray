from functools import cached_property

# docxray stuff
from docxray2.ns import MEDIA_TYPE, RELATIONSHIP_TYPE
from docxray2.opc.pkg_uri import PkgURI
from docxray2.oxml.shared_cxdp import E_DatastoreItem
from docxray2.proxy.custom_xml import CustomXml

from .base import DocxXmlPart


class CustomXmlDataPropertiesPart(DocxXmlPart[E_DatastoreItem]):
    ELEMENT = E_DatastoreItem
    PART_NAME_DEFAULT = PkgURI("/customXml/itemProps{n}.xml")
    CONTENT_TYPE_DEFAULT = MEDIA_TYPE.CUSTOM_XML
    RELATIONSHIP_TYPE_DEFAULT = RELATIONSHIP_TYPE.CUSTOM_XML

    @cached_property
    def custom_xml(self) -> CustomXml:
        return CustomXml(self.element, self)
