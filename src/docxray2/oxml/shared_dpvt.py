from __future__ import annotations

from decimal import Decimal

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.simple_types.shared_cst import ST_Guid
from docxray2.simple_types.shared_dpvt import (
    ST_ArrayBaseType,
    ST_Cy,
    ST_Error,
    ST_VectorBaseType,
)
from docxray2.xmlchemy import AttrOptional, AttrRequired, Content, Nsmap
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

NSMAP: Nsmap = {None: NAMESPACE.VARIANT_TYPES}


class OxmlNSDocumentPropertiesVariantTypes(Oxml, nsmap=NSMAP):
    pass


class CT_Empty(OxmlNSDocumentPropertiesVariantTypes):
    pass


class CT_Null(OxmlNSDocumentPropertiesVariantTypes):
    pass


class CT_Vector(OxmlNSDocumentPropertiesVariantTypes):
    base_type = AttrRequired("baseType", ST_VectorBaseType)
    size = AttrRequired("size", XsdUnsignedInt)

    @property
    def vectors(self) -> list[Vector]:
        return self.choice_many_at_least_one(
            E_Variant,
            E_I1,
            E_I2,
            E_I4,
            E_I8,
            E_Ui1,
            E_Ui2,
            E_Ui4,
            E_Ui8,
            E_R4,
            E_R8,
            E_Lpstr,
            E_Lpwstr,
            E_Bstr,
            E_Date,
            E_Filetime,
            E_Bool,
            E_Cy,
            E_Error,
            E_Clsid,
        )


class CT_Array(OxmlNSDocumentPropertiesVariantTypes):
    l_bounds = AttrRequired("lBounds", XsdInt)
    u_bounds = AttrRequired("uBounds", XsdInt)
    base_type = AttrRequired("baseType", ST_ArrayBaseType)

    @property
    def arrays(self) -> list[Array]:
        return self.choice_many_at_least_one(
            E_Variant,
            E_I1,
            E_I2,
            E_I4,
            E_Int,
            E_Ui1,
            E_Ui2,
            E_Ui4,
            E_Uint,
            E_R4,
            E_R8,
            E_Decimal,
            E_Bstr,
            E_Date,
            E_Bool,
            E_Error,
            E_Cy,
        )


class CT_Variant(OxmlNSDocumentPropertiesVariantTypes):
    @property
    def variant(self) -> Variant:
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
    content = Content(XsdString[str])


class E_Lpwstr(OxmlNSDocumentPropertiesVariantTypes, tag="lpwstr"):
    content = Content(XsdString[str])


class E_Bstr(OxmlNSDocumentPropertiesVariantTypes, tag="bstr"):
    content = Content(XsdString[str])


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


type Vector = (
    E_Variant
    | E_I1
    | E_I2
    | E_I4
    | E_I8
    | E_Ui1
    | E_Ui2
    | E_Ui4
    | E_Ui8
    | E_R4
    | E_R8
    | E_Lpstr
    | E_Lpwstr
    | E_Bstr
    | E_Date
    | E_Filetime
    | E_Bool
    | E_Cy
    | E_Error
    | E_Clsid
)


type Array = (
    E_Variant
    | E_I1
    | E_I2
    | E_I4
    | E_Int
    | E_Ui1
    | E_Ui2
    | E_Ui4
    | E_Uint
    | E_R4
    | E_R8
    | E_Decimal
    | E_Bstr
    | E_Date
    | E_Bool
    | E_Error
    | E_Cy
)
