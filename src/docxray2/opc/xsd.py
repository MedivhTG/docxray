import re

from ..xsd.simple_type import Restriction, SimpleType
from ..xsd.st_primitives import XsdString

ST_EXTENSION_PATTERN = re.compile(
    r"([!$&amp;'\(\)\*\+,:=]|(%[0-9a-fA-F][0-9a-fA-F])|[:@]|[a-zA-Z0-9\-_~])+"
)


class ST_Extension(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": ST_EXTENSION_PATTERN}


_TOKEN = r"[!#$%&'*+\-.0-9A-Z^_`a-z|~]"
_QUOTED_CHAR = r"[\x20-\x21\x23-\x7e\x80-\xff]|\s|\\[\x00-\x7f]"
ST_CONTENT_TYPE_PATTERN = re.compile(
    rf"((({_TOKEN})+)/(({_TOKEN})+)"
    rf"((\s+)*;(\s+)*"
    rf"((({_TOKEN})+)=((({_TOKEN})+)|\"({_QUOTED_CHAR})*\"))"
    rf")*)"
)


class ST_ContentType(SimpleType[str]):
    SCHEMA = Restriction(XsdString)
    FACETS = {"pattern": ST_CONTENT_TYPE_PATTERN}
