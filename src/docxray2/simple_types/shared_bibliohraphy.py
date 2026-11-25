# docxray stuff
from docxray2.xsd.simple_type import Restriction, SimpleType

from .enums import SE_SOURCE_TYPE
from .shared_cst import ST_String


class ST_SourceType(SimpleType[SE_SOURCE_TYPE]):
    SCHEMA = Restriction(ST_String)
    FACETS = {"enumeration": SE_SOURCE_TYPE}
