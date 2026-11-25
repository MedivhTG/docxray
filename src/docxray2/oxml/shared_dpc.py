from __future__ import annotations

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import AttrOptional, AttrRequired
from docxray2.xsd.primitives import XsdInt, XsdString

from .parser import Oxml
from .shared_cst import ST_Guid
from .shared_dpvt import (
    E_I1,
    E_I2,
    E_I4,
    E_I8,
    E_R4,
    E_R8,
    E_Array,
    E_Blob,
    E_Bool,
    E_Bstr,
    E_Clsid,
    E_Cy,
    E_Date,
    E_Decimal,
    E_Empty,
    E_Error,
    E_Filetime,
    E_Int,
    E_Lpstr,
    E_Lpwstr,
    E_Null,
    E_Oblob,
    E_Ostorage,
    E_Ostream,
    E_Storage,
    E_Stream,
    E_Ui1,
    E_Ui2,
    E_Ui4,
    E_Ui8,
    E_Uint,
    E_Vector,
    E_Vstream,
)

NSMAP = {
    None: NAMESPACE.CUSTOM_PROPERTIES,
    "vt": NAMESPACE.VARIANT_TYPES,
}


class OxmlNSDocumentPropertiesCustom(Oxml, nsmap=NSMAP):
    pass


class CT_Properties(OxmlNSDocumentPropertiesCustom):
    @property
    def properties(self) -> list[E_Property]:
        return self.all(E_Property)


class CT_Property(OxmlNSDocumentPropertiesCustom):
    fmtid = AttrRequired("fmtid", ST_Guid)
    pid = AttrRequired("pid", XsdInt)
    name = AttrOptional("name", XsdString[str])
    link_target = AttrOptional("linkTarget", XsdString[str])

    @property
    def value(self) -> PropertyValue:
        return self.choice_one(
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


# -------------------- ELEMENTS --------------------


class E_Properties(CT_Properties, tag="Properties"):
    pass


class E_Property(CT_Property, tag="property"):
    pass


type PropertyValue = E_Vector | E_Array | E_Blob | E_Oblob | E_Empty | E_Null | E_I1 | E_I2 | E_I4 | E_I8 | E_Int | E_Ui1 | E_Ui2 | E_Ui4 | E_Ui8 | E_Uint | E_R4 | E_R8 | E_Decimal | E_Lpstr | E_Lpwstr | E_Bstr | E_Date | E_Filetime | E_Bool | E_Cy | E_Error | E_Stream | E_Ostream | E_Storage | E_Ostorage | E_Vstream | E_Clsid
