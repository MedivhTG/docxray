# docxray stuff
from docxray2.oxml.elements.core_properties import E_CoreProperties

from .xml import XmlPart


class CorePropertiesPart(XmlPart):
    ELEMENT = E_CoreProperties
