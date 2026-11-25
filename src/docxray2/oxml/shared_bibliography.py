from __future__ import annotations

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.oxml.parser import Oxml
from docxray2.simple_types.shared_cst import ST_String
from docxray2.xmlchemy import Content, Nsmap

NSMAP: Nsmap = {"b": NAMESPACE.BIBLIOGRAPHY}


class OxmlNSBibliography(Oxml, ns="b", nsmap=NSMAP):
    pass


class CT_NameListType(OxmlNSBibliography):
    @property
    def person(self) -> list[E_Person]:
        return self.one_or_more(E_Person)


class CT_PersonType(OxmlNSBibliography):
    @property
    def person_types(self) -> list[E_Last | E_First | E_Middle]:
        return self.sequence(
            (E_Last, 0, "unbounded"),
            (E_First, 0, "unbounded"),
            (E_Middle, 0, "unbounded"),
        )


class CT_NameType(OxmlNSBibliography):
    @property
    def name_list(self) -> E_NameList:
        return self.one(E_NameList)


class CT_NameOrCorporateType(OxmlNSBibliography):
    pass


class CT_AuthorType(OxmlNSBibliography):
    pass


class CT_SourceType(OxmlNSBibliography):
    pass


class CT_Sources(OxmlNSBibliography):
    pass


# -------------------- ELEMENTS --------------------


class E_Sources(CT_Sources, tag="Sources"):
    pass


class E_Person(CT_PersonType, tag="Person"):
    pass


class E_Last(OxmlNSBibliography, tag="Last"):
    content = Content(ST_String)


class E_First(OxmlNSBibliography, tag="First"):
    content = Content(ST_String)


class E_Middle(OxmlNSBibliography, tag="Middle"):
    content = Content(ST_String)


class E_NameList(CT_NameListType, tag="NameList"):
    pass
