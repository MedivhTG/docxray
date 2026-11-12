# docxray stuff
from docxray2.xsd.primitives import (
    XsdDate,
    XsdDateTime,
    XsdGYear,
    XsdGYearMonth,
)
from docxray2.xsd.simple_type import SimpleType, Union
from docxray2.xsd.w3cdtf import W3CDTFDateTime


class W3CDTF(SimpleType[W3CDTFDateTime]):
    SCHEMA = Union(XsdDateTime, XsdDate, XsdGYearMonth, XsdGYear)
