from functools import cached_property

# docxray stuff
from docxray.oxml.t.ns import A, NoNS
from docxray.oxml.t.st.dml_main import ST_PitchFamily, ST_TextTypeface
from docxray.oxml.t.st.shared_common import ST_Panose
from docxray.oxml.t.xmlchemy import OxmlElement
from docxray.xsd.primitives import XsdByte

from .shared import CT_OfficeArtExtensionList


class CT_TextFont(OxmlElement):
    @cached_property
    def typeface(self) -> str:
        return self.attr_required(NoNS.TYPEFACE, ST_TextTypeface)

    @cached_property
    def panose(self) -> bytes:
        return self.attr_optional(NoNS.PANOSE, ST_Panose)

    @cached_property
    def pitchFamily(self) -> int:
        return self.attr_optional(NoNS.PITCH_FAMILY, ST_PitchFamily)

    @cached_property
    def charset(self) -> int:
        return self.attr_optional(NoNS.CHARSET, XsdByte, 1)


class CT_SupplementalFont(OxmlElement):
    @cached_property
    def script(self) -> str:
        return self.attr_required(NoNS.SCRIPT)

    @cached_property
    def typeface(self) -> str:
        return self.attr_required(NoNS.TYPEFACE, ST_TextTypeface)


class CT_FontCollection(OxmlElement):
    @cached_property
    def latin(self) -> CT_TextFont:
        return self.child_exactly_one(A.LATIN, CT_TextFont)

    @cached_property
    def ea(self) -> CT_TextFont:
        return self.child_exactly_one(A.EA, CT_TextFont)

    @cached_property
    def cs(self) -> CT_TextFont:
        return self.child_exactly_one(A.CS, CT_TextFont)

    @cached_property
    def font(self) -> list[CT_SupplementalFont]:
        return self.child_zero_or_more(A.FONT, CT_SupplementalFont)

    @cached_property
    def extLst(self) -> CT_OfficeArtExtensionList | None:
        return self.child_zero_or_one(A.EXT_LST, CT_OfficeArtExtensionList)


class CT_FontScheme(OxmlElement):
    @cached_property
    def majorFont(self) -> CT_FontCollection:
        return self.child_exactly_one(A.MAJOR_FONT, CT_FontCollection)

    @cached_property
    def minorFont(self) -> CT_FontCollection:
        return self.child_exactly_one(A.MINOR_FONT, CT_FontCollection)

    @cached_property
    def extLst(self) -> CT_OfficeArtExtensionList | None:
        return self.child_zero_or_one(A.EXT_LST, CT_OfficeArtExtensionList)
