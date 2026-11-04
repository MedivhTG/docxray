from __future__ import annotations

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.xmlchemy import Content
from docxray2.xsd.st_primitives import XsdDateTime, XsdString


class OxmlNSCoreProperties(Oxml, ns="cp"):
    pass


# TODO: extend elements (uncomment, add all)
class CT_CoreProperties(OxmlNSCoreProperties):
    @property
    def category(self) -> E_Category | None:
        return self.zero_or_one(E_Category)

    @property
    def content_status(self) -> E_ContentStatus | None:
        return self.zero_or_one(E_ContentStatus)

    # @property
    # def keywords(self) -> CT_Keywords | None:
    #     return self.zero_or_one(CT_Keywords)

    @property
    def last_modified_by(self) -> E_LastModifiedBy | None:
        return self.zero_or_one(E_LastModifiedBy)

    # @property
    # def last_printed(self) -> E_LastPrinted | None:
    #     return self.zero_or_one(E_LastPrinted)

    @property
    def revision(self) -> E_Revision | None:
        return self.zero_or_one(E_Revision)

    @property
    def version(self) -> E_Version | None:
        return self.zero_or_one(E_Version)


# -------------------- ELEMENTS --------------------


class E_CoreProperties(CT_CoreProperties, tag="coreProperties"):
    pass


class E_Category(OxmlNSCoreProperties, tag="category"):
    content = Content(XsdString[str])


class E_ContentStatus(OxmlNSCoreProperties, tag="contentStatus"):
    content = Content(XsdString[str])


# TODO: realise
# class E_Keywords(OxmlNSCoreProperties, tag="keywords"):
#     # complex type CT_Keywords — не простой текст
#     ...


class E_LastModifiedBy(OxmlNSCoreProperties, tag="lastModifiedBy"):
    content = Content(XsdString[str])


class E_LastPrinted(OxmlNSCoreProperties, tag="lastPrinted"):
    content = Content(XsdDateTime)


class E_Revision(OxmlNSCoreProperties, tag="revision"):
    content = Content(XsdString[str])


class E_Version(OxmlNSCoreProperties, tag="version"):
    content = Content(XsdString[str])
