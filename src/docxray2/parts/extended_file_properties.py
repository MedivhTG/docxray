# docxray stuff

# docxray stuff
from docxray2.oxml.xml.extended_file_properties import E_Properties

from .xml import XmlPart


class ExtendedFilePropertiesPart(XmlPart):
    ELEMENT = E_Properties
