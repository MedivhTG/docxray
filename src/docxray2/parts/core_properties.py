# docxray stuff

# docxray stuff
from docxray2.oxml.xml.core_properties import E_CoreProperties

from .base import DocxXmlPart


class CorePropertiesPart(DocxXmlPart):
    ELEMENT = E_CoreProperties
