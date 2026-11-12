import re

# docxray stuff
from docxray2.xsd.primitives import XsdToken
from docxray2.xsd.simple_type import Restriction, SimpleType

GUID_RE = re.compile(
    r"\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}"
)


class ST_Guid(SimpleType[str]):
    SCHEMA = Restriction(XsdToken[str])
    FACETS = {"enumeration": GUID_RE}
