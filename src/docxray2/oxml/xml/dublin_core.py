# mypy: disable-error-code="var-annotated"
# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.oxml.xsd.dublin_core import W3CDTF
from docxray2.xmlchemy import AttrRequired, Content
from docxray2.xsd.st_primitives import XsdString


class OxmlNSDublinCore(Oxml, ns="dc"):
    pass


class OxmlNSDublinCoreTerms(Oxml, ns="dcterms"):
    pass


class CT_W3CDTF(OxmlNSDublinCoreTerms):
    content = Content(W3CDTF)


# -------------------- ELEMENTS --------------------


class E_Creator(OxmlNSDublinCore, tag="creator"):
    content = Content(XsdString)


class E_Description(OxmlNSDublinCore, tag="description"):
    content = Content(XsdString)


class E_Identifier(OxmlNSDublinCore, tag="identifier"):
    content = Content(XsdString)


class E_Language(OxmlNSDublinCore, tag="language"):
    content = Content(XsdString)


class E_Subject(OxmlNSDublinCore, tag="subject"):
    content = Content(XsdString)


class E_Title(OxmlNSDublinCore, tag="title"):
    content = Content(XsdString)


class E_Created(CT_W3CDTF, tag="created"):
    schemaType = AttrRequired("xsi:type", fixed="dcterms:W3CDTF")


class E_Modified(CT_W3CDTF, tag="modified"):
    schemaType = AttrRequired("xsi:type", fixed="dcterms:W3CDTF")
