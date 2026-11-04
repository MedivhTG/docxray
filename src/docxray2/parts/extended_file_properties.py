# docxray stuff

# docxray stuff
from docxray2.oxml.xml.extended_file_properties import E_Properties

from .base import DocxXmlPart


class ExtendedFilePropertiesPart(DocxXmlPart):
    ELEMENT = E_Properties
