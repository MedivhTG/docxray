from __future__ import annotations

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.xmlchemy import Content
from docxray2.xsd.primitives import XsdInt, XsdString


class OxmlNSExtendedFileProperties(Oxml, ns="ep"):
    pass


class CT_Properties(OxmlNSExtendedFileProperties):
    @property
    def pages(self) -> E_Pages | None:
        return self.zero_or_one(E_Pages)


# -------------------- ELEMENTS --------------------


class E_Properties(CT_Properties, tag="Properties"):
    pass


class E_Template(OxmlNSExtendedFileProperties, tag="Template"):
    content = Content(XsdString[str])


class E_Manager(OxmlNSExtendedFileProperties, tag="Manager"):
    content = Content(XsdString[str])


class E_Company(OxmlNSExtendedFileProperties, tag="Company"):
    content = Content(XsdString[str])


class E_Pages(OxmlNSExtendedFileProperties, tag="Pages"):
    content = Content(XsdInt)


class E_Words(OxmlNSExtendedFileProperties, tag="Words"):
    content = Content(XsdInt)


class E_Characters(OxmlNSExtendedFileProperties, tag="Characters"):
    content = Content(XsdInt)


class E_PresentationFormat(
    OxmlNSExtendedFileProperties, tag="PresentationFormat"
):
    content = Content(XsdString[str])


class E_Lines(OxmlNSExtendedFileProperties, tag="Lines"):
    content = Content(XsdInt)


class E_Paragraphs(OxmlNSExtendedFileProperties, tag="Paragraphs"):
    content = Content(XsdInt)


class E_Slides(OxmlNSExtendedFileProperties, tag="Slides"):
    content = Content(XsdInt)


class E_Notes(OxmlNSExtendedFileProperties, tag="Notes"):
    content = Content(XsdInt)


class E_TotalTime(OxmlNSExtendedFileProperties, tag="TotalTime"):
    content = Content(XsdInt)


class E_HiddenSlides(OxmlNSExtendedFileProperties, tag="HiddenSlides"):
    content = Content(XsdInt)


class E_MMClips(OxmlNSExtendedFileProperties, tag="MMClips"):
    content = Content(XsdInt)


# class E_ScaleCrop(OxmlNSExtendedFileProperties, tag="ScaleCrop"):
#     content = Content(XsdBoolean)


# class E_HeadingPairs(OxmlNSExtendedFileProperties, tag="HeadingPairs"):
#     pass


# class E_TitlesOfParts(OxmlNSExtendedFileProperties, tag="TitlesOfParts"):
#     pass


# class E_LinksUpToDate(OxmlNSExtendedFileProperties, tag="LinksUpToDate"):
#     content = Content(XsdBoolean)


class E_CharactersWithSpaces(
    OxmlNSExtendedFileProperties, tag="CharactersWithSpaces"
):
    content = Content(XsdInt)


# class E_SharedDoc(OxmlNSExtendedFileProperties, tag="SharedDoc"):
#     content = Content(XsdBoolean)


class E_HyperlinkBase(OxmlNSExtendedFileProperties, tag="HyperlinkBase"):
    content = Content(XsdString[str])


# class E_HLinks(OxmlNSExtendedFileProperties, tag="HLinks"):
#     pass


# class E_HyperlinksChanged(
#     OxmlNSExtendedFileProperties, tag="HyperlinksChanged"
# ):
#     content = Content(XsdBoolean)


# class E_DigSig(OxmlNSExtendedFileProperties, tag="DigSig"):
#     pass


class E_Application(OxmlNSExtendedFileProperties, tag="Application"):
    content = Content(XsdString[str])


class E_AppVersion(OxmlNSExtendedFileProperties, tag="AppVersion"):
    content = Content(XsdString[str])


class E_DocSecurity(OxmlNSExtendedFileProperties, tag="DocSecurity"):
    content = Content(XsdInt)
