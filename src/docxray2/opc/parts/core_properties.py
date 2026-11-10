from functools import cached_property

# docxray stuff
from docxray2.ns import MEDIA_TYPE, NAMESPACE, RELATIONSHIP_TYPE
from docxray2.opc.oxml.core_properties import E_CoreProperties
from docxray2.opc.parts.base import OpcXmlPart
from docxray2.opc.pkg_uri import PkgURI
from docxray2.opc.proxy.core_props import CoreProperties


class CorePropertiesPart(OpcXmlPart[E_CoreProperties]):
    ELEMENT = E_CoreProperties
    PART_NAME_DEFAULT = PkgURI("/docProps/core.xml")
    CONTENT_TYPE_DEFAULT = MEDIA_TYPE.CORE_PROPERTIES
    RELATIONSHIP_TYPE_DEFAULT = RELATIONSHIP_TYPE.CORE_PROPERTIES
    NSMAP_DEFAULT = {
        "cp": NAMESPACE.CORE_PROPERTIES,
        "dc": NAMESPACE.DUBLIN_CORE,
        "dcterms": NAMESPACE.DUBLIN_CORE_TERMS,
        "xsi": NAMESPACE.XML_SHEMA_INSTANCE,
    }

    @cached_property
    def core_props(self) -> CoreProperties:
        return CoreProperties(self.element, self)
