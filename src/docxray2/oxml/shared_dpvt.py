from __future__ import annotations

from decimal import Decimal

# docxray stuff
from docxray2.oxml.shared_common_st import ST_Guid
from docxray2.simple_types.shared_dpvt import (
    ST_ArrayBaseType,
    ST_Cy,
    ST_Error,
    ST_VectorBaseType,
)
from docxray2.xmlchemy import AttrOptional, AttrRequired, Content
from docxray2.xsd.primitives import (
    XsdBase64Binary,
    XsdBoolean,
    XsdByte,
    XsdDateTime,
    XsdDecimal,
    XsdDouble,
    XsdFloat,
    XsdInt,
    XsdLong,
    XsdShort,
    XsdString,
    XsdUnsignedByte,
    XsdUnsignedInt,
    XsdUnsignedLong,
    XsdUnsignedShort,
)

from .parser import Oxml


class OxmlNSDocumentPropertiesVariantTypes(Oxml, ns="vt"):
    pass


class CT_Empty(OxmlNSDocumentPropertiesVariantTypes):
    pass


class CT_Null(OxmlNSDocumentPropertiesVariantTypes):
    pass


class CT_Vector(OxmlNSDocumentPropertiesVariantTypes):
    base_type = AttrRequired("baseType", ST_VectorBaseType)
    size = AttrRequired("size", XsdUnsignedInt)

    @property
    def variant(self) -> list[E_Variant]:
        return self.zero_or_more(E_Variant)

    @property
    def i1(self) -> list[E_I1]:
        return self.zero_or_more(E_I1)

    @property
    def i2(self) -> list[E_I2]:
        return self.zero_or_more(E_I2)

    @property
    def i4(self) -> list[E_I4]:
        return self.zero_or_more(E_I4)

    @property
    def i8(self) -> list[E_I8]:
        return self.zero_or_more(E_I8)

    @property
    def ui1(self) -> list[E_Ui1]:
        return self.zero_or_more(E_Ui1)

    @property
    def ui2(self) -> list[E_Ui2]:
        return self.zero_or_more(E_Ui2)

    @property
    def ui4(self) -> list[E_Ui4]:
        return self.zero_or_more(E_Ui4)

    @property
    def ui8(self) -> list[E_Ui8]:
        return self.zero_or_more(E_Ui8)

    @property
    def r4(self) -> list[E_R4]:
        return self.zero_or_more(E_R4)

    @property
    def r8(self) -> list[E_R8]:
        return self.zero_or_more(E_R8)

    @property
    def lpstr(self) -> list[E_Lpstr]:
        return self.zero_or_more(E_Lpstr)

    @property
    def lpwstr(self) -> list[E_Lpwstr]:
        return self.zero_or_more(E_Lpwstr)

    @property
    def bstr(self) -> list[E_Bstr]:
        return self.zero_or_more(E_Bstr)

    @property
    def date(self) -> list[E_Date]:
        return self.zero_or_more(E_Date)

    @property
    def filetime(self) -> list[E_Filetime]:
        return self.zero_or_more(E_Filetime)

    @property
    def bool(self) -> list[E_Bool]:
        return self.zero_or_more(E_Bool)

    @property
    def cy(self) -> list[E_Cy]:
        return self.zero_or_more(E_Cy)

    @property
    def error(self) -> list[E_Error]:
        return self.zero_or_more(E_Error)

    @property
    def clsid(self) -> list[E_Clsid]:
        return self.zero_or_more(E_Clsid)


class CT_Array(OxmlNSDocumentPropertiesVariantTypes):
    l_bounds = AttrRequired("lBounds", XsdInt)
    u_bounds = AttrRequired("uBounds", XsdInt)
    base_type = AttrRequired("baseType", ST_ArrayBaseType)

    @property
    def variant(self) -> list[E_Variant]:
        return self.zero_or_more(E_Variant)

    @property
    def i1(self) -> list[E_I1]:
        return self.zero_or_more(E_I1)

    @property
    def i2(self) -> list[E_I2]:
        return self.zero_or_more(E_I2)

    @property
    def i4(self) -> list[E_I4]:
        return self.zero_or_more(E_I4)

    @property
    def int(self) -> list[E_Int]:
        return self.zero_or_more(E_Int)

    @property
    def ui1(self) -> list[E_Ui1]:
        return self.zero_or_more(E_Ui1)

    @property
    def ui2(self) -> list[E_Ui2]:
        return self.zero_or_more(E_Ui2)

    @property
    def ui4(self) -> list[E_Ui4]:
        return self.zero_or_more(E_Ui4)

    @property
    def uint(self) -> list[E_Uint]:
        return self.zero_or_more(E_Uint)

    @property
    def r4(self) -> list[E_R4]:
        return self.zero_or_more(E_R4)

    @property
    def r8(self) -> list[E_R8]:
        return self.zero_or_more(E_R8)

    @property
    def decimal(self) -> list[E_Decimal]:
        return self.zero_or_more(E_Decimal)

    @property
    def bstr(self) -> list[E_Bstr]:
        return self.zero_or_more(E_Bstr)

    @property
    def date(self) -> list[E_Date]:
        return self.zero_or_more(E_Date)

    @property
    def bool(self) -> list[E_Bool]:
        return self.zero_or_more(E_Bool)

    @property
    def error(self) -> list[E_Error]:
        return self.zero_or_more(E_Error)

    @property
    def cy(self) -> list[E_Cy]:
        return self.zero_or_more(E_Cy)


class CT_Variant(OxmlNSDocumentPropertiesVariantTypes):
    @property
    def chosen_variant(self) -> Variant:
        return self.choice_one(
            E_Variant,
            E_Vector,
            E_Array,
            E_Blob,
            E_Oblob,
            E_Empty,
            E_Null,
            E_I1,
            E_I2,
            E_I4,
            E_I8,
            E_Int,
            E_Ui1,
            E_Ui2,
            E_Ui4,
            E_Ui8,
            E_Uint,
            E_R4,
            E_R8,
            E_Decimal,
            E_Lpstr,
            E_Lpwstr,
            E_Bstr,
            E_Date,
            E_Filetime,
            E_Bool,
            E_Cy,
            E_Error,
            E_Stream,
            E_Ostream,
            E_Storage,
            E_Ostorage,
            E_Vstream,
            E_Clsid,
        )  # type: ignore[return-value]


class CT_Vstream(OxmlNSDocumentPropertiesVariantTypes):
    version = AttrOptional("version", ST_Guid)


# -------------------- ELEMENTS --------------------


class E_Variant(CT_Variant, tag="variant"):
    pass


class E_Vector(CT_Vector, tag="vector"):
    pass


class E_Array(CT_Array, tag="array"):
    pass


class E_Blob(OxmlNSDocumentPropertiesVariantTypes, tag="blob"):
    content = Content(XsdBase64Binary)


class E_Oblob(OxmlNSDocumentPropertiesVariantTypes, tag="oblob"):
    content = Content(XsdBase64Binary)


class E_Empty(CT_Empty, tag="empty"):
    pass


class E_Null(CT_Null, tag="null"):
    pass


class E_I1(OxmlNSDocumentPropertiesVariantTypes, tag="i1"):
    content = Content(XsdByte)


class E_I2(OxmlNSDocumentPropertiesVariantTypes, tag="i2"):
    content = Content(XsdShort)


class E_I4(OxmlNSDocumentPropertiesVariantTypes, tag="i4"):
    content = Content(XsdInt)


class E_I8(OxmlNSDocumentPropertiesVariantTypes, tag="i8"):
    content = Content(XsdLong)


class E_Int(OxmlNSDocumentPropertiesVariantTypes, tag="int"):
    content = Content(XsdInt)


class E_Ui1(OxmlNSDocumentPropertiesVariantTypes, tag="ui1"):
    content = Content(XsdUnsignedByte)


class E_Ui2(OxmlNSDocumentPropertiesVariantTypes, tag="ui2"):
    content = Content(XsdUnsignedShort)


class E_Ui4(OxmlNSDocumentPropertiesVariantTypes, tag="ui4"):
    content = Content(XsdUnsignedInt)


class E_Ui8(OxmlNSDocumentPropertiesVariantTypes, tag="ui8"):
    content = Content(XsdUnsignedLong)


class E_Uint(OxmlNSDocumentPropertiesVariantTypes, tag="uint"):
    content = Content(XsdUnsignedInt)


class E_R4(OxmlNSDocumentPropertiesVariantTypes, tag="r4"):
    content = Content(XsdFloat)


class E_R8(OxmlNSDocumentPropertiesVariantTypes, tag="r8"):
    content = Content(XsdDouble)


class E_Decimal(OxmlNSDocumentPropertiesVariantTypes, tag="decimal"):
    content = Content(XsdDecimal[Decimal])


class E_Lpstr(OxmlNSDocumentPropertiesVariantTypes, tag="lpstr"):
    content = Content(XsdString)


class E_Lpwstr(OxmlNSDocumentPropertiesVariantTypes, tag="lpwstr"):
    content = Content(XsdString)


class E_Bstr(OxmlNSDocumentPropertiesVariantTypes, tag="bstr"):
    content = Content(XsdString)


class E_Date(OxmlNSDocumentPropertiesVariantTypes, tag="date"):
    content = Content(XsdDateTime)


class E_Filetime(OxmlNSDocumentPropertiesVariantTypes, tag="filetime"):
    content = Content(XsdDateTime)


class E_Bool(OxmlNSDocumentPropertiesVariantTypes, tag="bool"):
    content = Content(XsdBoolean)


class E_Cy(OxmlNSDocumentPropertiesVariantTypes, tag="cy"):
    content = Content(ST_Cy)


class E_Error(OxmlNSDocumentPropertiesVariantTypes, tag="error"):
    content = Content(ST_Error)


class E_Stream(OxmlNSDocumentPropertiesVariantTypes, tag="stream"):
    content = Content(XsdBase64Binary)


class E_Ostream(OxmlNSDocumentPropertiesVariantTypes, tag="ostream"):
    content = Content(XsdBase64Binary)


class E_Storage(OxmlNSDocumentPropertiesVariantTypes, tag="storage"):
    content = Content(XsdBase64Binary)


class E_Ostorage(OxmlNSDocumentPropertiesVariantTypes, tag="ostorage"):
    content = Content(XsdBase64Binary)


class E_Vstream(CT_Vstream, tag="vstream"):
    pass


class E_Clsid(OxmlNSDocumentPropertiesVariantTypes, tag="clsid"):
    content = Content(ST_Guid)


type Variant = (
    E_Variant
    | E_Vector
    | E_Array
    | E_Blob
    | E_Oblob
    | E_Empty
    | E_Null
    | E_I1
    | E_I2
    | E_I4
    | E_I8
    | E_Int
    | E_Ui1
    | E_Ui2
    | E_Ui4
    | E_Ui8
    | E_Uint
    | E_R4
    | E_R8
    | E_Decimal
    | E_Lpstr
    | E_Lpwstr
    | E_Bstr
    | E_Date
    | E_Filetime
    | E_Bool
    | E_Cy
    | E_Error
    | E_Stream
    | E_Ostream
    | E_Storage
    | E_Ostorage
    | E_Vstream
    | E_Clsid
)
