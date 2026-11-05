# mypy: disable-error-code="var-annotated"
from __future__ import annotations

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.xmlchemy import AttrOptional, Content
from docxray2.xsd.st_primitives import XsdDateTime, XsdString

from .dublin_core import (
    E_Created,
    E_Creator,
    E_Description,
    E_Identifier,
    E_Language,
    E_Modified,
    E_Subject,
    E_Title,
)


class OxmlNSCoreProperties(Oxml, ns="cp"):
    pass


class CT_CoreProperties(OxmlNSCoreProperties):
    @property
    def category(self) -> E_Category | None:
        return self.zero_or_one(E_Category)

    @property
    def contentStatus(self) -> E_ContentStatus | None:
        return self.zero_or_one(E_ContentStatus)

    @property
    def created(self) -> E_Created | None:
        return self.zero_or_one(E_Created)

    @property
    def creator(self) -> E_Creator | None:
        return self.zero_or_one(E_Creator)

    @property
    def description(self) -> E_Description | None:
        return self.zero_or_one(E_Description)

    @property
    def identifier(self) -> E_Identifier | None:
        return self.zero_or_one(E_Identifier)

    @property
    def keywords(self) -> E_Keywords | None:
        return self.zero_or_one(E_Keywords)

    @property
    def language(self) -> E_Language | None:
        return self.zero_or_one(E_Language)

    @property
    def lastModifiedBy(self) -> E_LastModifiedBy | None:
        return self.zero_or_one(E_LastModifiedBy)

    @property
    def lastPrinted(self) -> E_LastPrinted | None:
        return self.zero_or_one(E_LastPrinted)

    @property
    def modified(self) -> E_Modified | None:
        return self.zero_or_one(E_Modified)

    @property
    def revision(self) -> E_Revision | None:
        return self.zero_or_one(E_Revision)

    @property
    def subject(self) -> E_Subject | None:
        return self.zero_or_one(E_Subject)

    @property
    def title(self) -> E_Title | None:
        return self.zero_or_one(E_Title)

    @property
    def version(self) -> E_Version | None:
        return self.zero_or_one(E_Version)


# MIXED
class CT_Keywords(OxmlNSCoreProperties):
    content = Content()

    @property
    def keywords(self) -> list[E_Value]:
        return self.zero_or_more(E_Value)


class CT_Keyword(OxmlNSCoreProperties):
    lang = AttrOptional("xml:lang")
    content = Content()


# -------------------- ELEMENTS --------------------


class E_CoreProperties(CT_CoreProperties, tag="coreProperties"):
    pass


class E_Category(OxmlNSCoreProperties, tag="category"):
    content = Content(XsdString[str])


class E_ContentStatus(OxmlNSCoreProperties, tag="contentStatus"):
    content = Content(XsdString[str])


class E_Keywords(CT_Keywords, tag="keywords"):
    pass


class E_Value(CT_Keyword, tag="value"):
    pass


class E_LastModifiedBy(OxmlNSCoreProperties, tag="lastModifiedBy"):
    content = Content(XsdString[str])


class E_LastPrinted(OxmlNSCoreProperties, tag="lastPrinted"):
    content = Content(XsdDateTime)


class E_Revision(OxmlNSCoreProperties, tag="revision"):
    content = Content(XsdString[str])


class E_Version(OxmlNSCoreProperties, tag="version"):
    content = Content(XsdString[str])
