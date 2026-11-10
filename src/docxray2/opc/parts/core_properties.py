from functools import cached_property

# docxray stuff
from docxray2.opc.oxml.core_properties import E_CoreProperties
from docxray2.opc.parts.base import OpcXmlPart
from docxray2.opc.proxy.core_props import CoreProperties


class CorePropertiesPart(OpcXmlPart[E_CoreProperties]):
    ELEMENT = E_CoreProperties

    @cached_property
    def core_props(self) -> CoreProperties:
        return CoreProperties(self.element, self)
