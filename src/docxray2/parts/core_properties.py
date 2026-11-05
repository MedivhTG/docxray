from functools import cached_property

# docxray stuff
from docxray2.oxml.proxy.core_props import CoreProperties
from docxray2.oxml.xml.core_properties import E_CoreProperties

from .base import DocxXmlPart


class CorePropertiesPart(DocxXmlPart[E_CoreProperties]):
    ELEMENT = E_CoreProperties

    @cached_property
    def core_props(self) -> CoreProperties:
        return CoreProperties(self.element, self)
