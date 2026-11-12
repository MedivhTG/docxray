# mypy: disable-error-code="var-annotated"


# docxray stuff
from docxray2.opc.xsd.dublin_core import W3CDTF
from docxray2.xmlchemy import AttrRequired, Content
from docxray2.xsd.primitives import XsdString

from .parser import OpcOxml


class OpcOxmlNSDublinCore(OpcOxml, ns="dc"):
    pass


class OpcOxmlNSDublinCoreTerms(OpcOxml, ns="dcterms"):
    pass


class CT_W3CDTF(OpcOxmlNSDublinCoreTerms):
    content = Content(W3CDTF)


# -------------------- ELEMENTS --------------------


class E_Creator(OpcOxmlNSDublinCore, tag="creator"):
    content = Content(XsdString[str])


class E_Description(OpcOxmlNSDublinCore, tag="description"):
    content = Content(XsdString[str])


class E_Identifier(OpcOxmlNSDublinCore, tag="identifier"):
    content = Content(XsdString[str])


class E_Language(OpcOxmlNSDublinCore, tag="language"):
    content = Content(XsdString[str])


class E_Subject(OpcOxmlNSDublinCore, tag="subject"):
    content = Content(XsdString[str])


class E_Title(OpcOxmlNSDublinCore, tag="title"):
    content = Content(XsdString[str])


class E_Created(CT_W3CDTF, tag="created"):
    schemaType = AttrRequired("xsi:type", fixed="dcterms:W3CDTF")


class E_Modified(CT_W3CDTF, tag="modified"):
    schemaType = AttrRequired("xsi:type", fixed="dcterms:W3CDTF")
