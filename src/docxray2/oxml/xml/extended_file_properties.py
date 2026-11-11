from __future__ import annotations

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.xmlchemy import Content
from docxray2.xsd.st_primitives import XsdInt, XsdString


class OxmlNSExtendedFileProperties(Oxml, ns="ep"):
    pass


class CT_Properties(OxmlNSExtendedFileProperties):
    @property
    def pages(self) -> E_Pages | None:
        return self.zero_or_one(E_Pages)


# -------------------- ELEMENTS --------------------


class E_Properties(CT_Properties, tag="Properties"):
    pass


class E_Template(OxmlNSExtendedFileProperties):
    content = Content(XsdString[str])


class E_Manager(OxmlNSExtendedFileProperties):
    content = Content(XsdString[str])


class E_Company(OxmlNSExtendedFileProperties):
    content = Content(XsdString[str])


class E_Pages(OxmlNSExtendedFileProperties, tag="Pages"):
    content = Content(XsdInt)
