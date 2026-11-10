from datetime import datetime

# docxray stuff
from docxray2.xsd.simple_type import SimpleType, Union
from docxray2.xsd.st_primitives import XsdDateTime


# TODO: mb later, it's enough
# Member types (union): xs:gYear xs:gYearMonth xs:date xs:dateTime
class W3CDTF(SimpleType[datetime]):
    SCHEMA = Union(XsdDateTime)
