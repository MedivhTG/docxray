from __future__ import annotations

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import Content
from docxray2.xsd.primitives import XsdBoolean, XsdInt, XsdString

from .parser import Oxml
from .shared_dpvt import E_Blob, E_Vector

NSMAP = {
    None: NAMESPACE.EXTENDED_PROPERTIES,
    "vt": NAMESPACE.VARIANT_TYPES,
}


class OxmlNSDocumentPropertiesExtended(Oxml, nsmap=NSMAP):
    pass


class CT_Properties(OxmlNSDocumentPropertiesExtended):
    @property
    def template(self) -> E_Template | None:
        return self.one_or_none(E_Template)

    @property
    def manager(self) -> E_Manager | None:
        return self.one_or_none(E_Manager)

    @property
    def company(self) -> E_Company | None:
        return self.one_or_none(E_Company)

    @property
    def pages(self) -> E_Pages | None:
        return self.one_or_none(E_Pages)

    @property
    def words(self) -> E_Words | None:
        return self.one_or_none(E_Words)

    @property
    def characters(self) -> E_Characters | None:
        return self.one_or_none(E_Characters)

    @property
    def presentation_format(self) -> E_PresentationFormat | None:
        return self.one_or_none(E_PresentationFormat)

    @property
    def lines(self) -> E_Lines | None:
        return self.one_or_none(E_Lines)

    @property
    def paragraphs(self) -> E_Paragraphs | None:
        return self.one_or_none(E_Paragraphs)

    @property
    def slides(self) -> E_Slides | None:
        return self.one_or_none(E_Slides)

    @property
    def notes(self) -> E_Notes | None:
        return self.one_or_none(E_Notes)

    @property
    def total_time(self) -> E_TotalTime | None:
        return self.one_or_none(E_TotalTime)

    @property
    def hidden_slides(self) -> E_HiddenSlides | None:
        return self.one_or_none(E_HiddenSlides)

    @property
    def mm_clips(self) -> E_MMClips | None:
        return self.one_or_none(E_MMClips)

    @property
    def scale_crop(self) -> E_ScaleCrop | None:
        return self.one_or_none(E_ScaleCrop)

    @property
    def heading_pairs(self) -> E_HeadingPairs | None:
        return self.one_or_none(E_HeadingPairs)

    @property
    def titles_of_parts(self) -> E_TitlesOfParts | None:
        return self.one_or_none(E_TitlesOfParts)

    @property
    def links_up_to_date(self) -> E_LinksUpToDate | None:
        return self.one_or_none(E_LinksUpToDate)

    @property
    def characters_with_spaces(self) -> E_CharactersWithSpaces | None:
        return self.one_or_none(E_CharactersWithSpaces)

    @property
    def shared_doc(self) -> E_SharedDoc | None:
        return self.one_or_none(E_SharedDoc)

    @property
    def hyperlink_base(self) -> E_HyperlinkBase | None:
        return self.one_or_none(E_HyperlinkBase)

    @property
    def h_links(self) -> E_HLinks | None:
        return self.one_or_none(E_HLinks)

    @property
    def hyperlinks_changed(self) -> E_HyperlinksChanged | None:
        return self.one_or_none(E_HyperlinksChanged)

    @property
    def dig_sig(self) -> E_DigSig | None:
        return self.one_or_none(E_DigSig)

    @property
    def application(self) -> E_Application | None:
        return self.one_or_none(E_Application)

    @property
    def app_version(self) -> E_AppVersion | None:
        return self.one_or_none(E_AppVersion)

    @property
    def doc_security(self) -> E_DocSecurity | None:
        return self.one_or_none(E_DocSecurity)


class CT_VectorVariant(OxmlNSDocumentPropertiesExtended):
    @property
    def vector(self) -> E_Vector:
        return self.one(E_Vector)


class CT_VectorLpstr(OxmlNSDocumentPropertiesExtended):
    @property
    def vector(self) -> E_Vector:
        return self.one(E_Vector)


class CT_DigSigBlob(OxmlNSDocumentPropertiesExtended):
    @property
    def blob(self) -> E_Blob:
        return self.one(E_Blob)


# -------------------- ELEMENTS --------------------


class E_Properties(CT_Properties, tag="Properties"):
    pass


class E_Template(OxmlNSDocumentPropertiesExtended, tag="Template"):
    content = Content(XsdString[str])


class E_Manager(OxmlNSDocumentPropertiesExtended, tag="Manager"):
    content = Content(XsdString[str])


class E_Company(OxmlNSDocumentPropertiesExtended, tag="Company"):
    content = Content(XsdString[str])


class E_Pages(OxmlNSDocumentPropertiesExtended, tag="Pages"):
    content = Content(XsdInt)


class E_Words(OxmlNSDocumentPropertiesExtended, tag="Words"):
    content = Content(XsdInt)


class E_Characters(OxmlNSDocumentPropertiesExtended, tag="Characters"):
    content = Content(XsdInt)


class E_PresentationFormat(
    OxmlNSDocumentPropertiesExtended, tag="PresentationFormat"
):
    content = Content(XsdString[str])


class E_Lines(OxmlNSDocumentPropertiesExtended, tag="Lines"):
    content = Content(XsdInt)


class E_Paragraphs(OxmlNSDocumentPropertiesExtended, tag="Paragraphs"):
    content = Content(XsdInt)


class E_Slides(OxmlNSDocumentPropertiesExtended, tag="Slides"):
    content = Content(XsdInt)


class E_Notes(OxmlNSDocumentPropertiesExtended, tag="Notes"):
    content = Content(XsdInt)


class E_TotalTime(OxmlNSDocumentPropertiesExtended, tag="TotalTime"):
    content = Content(XsdInt)


class E_HiddenSlides(OxmlNSDocumentPropertiesExtended, tag="HiddenSlides"):
    content = Content(XsdInt)


class E_MMClips(OxmlNSDocumentPropertiesExtended, tag="MMClips"):
    content = Content(XsdInt)


class E_ScaleCrop(OxmlNSDocumentPropertiesExtended, tag="ScaleCrop"):
    content = Content(XsdBoolean)


class E_HeadingPairs(CT_VectorVariant, tag="HeadingPairs"):
    pass


class E_TitlesOfParts(CT_VectorLpstr, tag="TitlesOfParts"):
    pass


class E_LinksUpToDate(OxmlNSDocumentPropertiesExtended, tag="LinksUpToDate"):
    content = Content(XsdBoolean)


class E_CharactersWithSpaces(
    OxmlNSDocumentPropertiesExtended, tag="CharactersWithSpaces"
):
    content = Content(XsdInt)


class E_SharedDoc(OxmlNSDocumentPropertiesExtended, tag="SharedDoc"):
    content = Content(XsdBoolean)


class E_HyperlinkBase(OxmlNSDocumentPropertiesExtended, tag="HyperlinkBase"):
    content = Content(XsdString[str])


class E_HLinks(CT_VectorVariant, tag="HLinks"):
    pass


class E_HyperlinksChanged(
    OxmlNSDocumentPropertiesExtended, tag="HyperlinksChanged"
):
    content = Content(XsdBoolean)


class E_DigSig(CT_DigSigBlob, tag="DigSig"):
    pass


class E_Application(OxmlNSDocumentPropertiesExtended, tag="Application"):
    content = Content(XsdString[str])


class E_AppVersion(OxmlNSDocumentPropertiesExtended, tag="AppVersion"):
    content = Content(XsdString[str])


class E_DocSecurity(OxmlNSDocumentPropertiesExtended, tag="DocSecurity"):
    content = Content(XsdInt)
