# docxray stuff
from docxray2.xsd.simple_type import Restriction, SimpleType
from docxray2.xsd.st_primitives import XsdString

from .enums import SE_TARGET_MODE


class ST_TargetMode(SimpleType[SE_TARGET_MODE]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"enumeration": SE_TARGET_MODE}
