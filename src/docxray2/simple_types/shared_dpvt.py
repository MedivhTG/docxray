import re

# docxray stuff
from docxray2.simple_types.enums import SE_ARRAY_BASE_TYPE, SE_VECTOR_BASE_TYPE
from docxray2.xsd.primitives import XsdString
from docxray2.xsd.simple_type import Restriction, SimpleType


class ST_VectorBaseType(SimpleType[SE_VECTOR_BASE_TYPE]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"enumeration": SE_VECTOR_BASE_TYPE}


class ST_ArrayBaseType(SimpleType[SE_ARRAY_BASE_TYPE]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"enumeration": SE_ARRAY_BASE_TYPE}


CY_RE = re.compile(r"\s*[0-9]*\.[0-9]{4}\s*")


class ST_Cy(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": CY_RE}


ERROR_RE = re.compile(r"\s*0x[0-9A-Za-z]{8}\s*")


class ST_Error(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": ERROR_RE}
