from __future__ import annotations

# docxray stuff
from docxray2.ns import NAMESPACE_URI
from docxray2.opc.xsd.content_types import ST_ContentType, ST_Extension
from docxray2.xmlchemy import AttrRequired, Nsmap
from docxray2.xsd.primitives import XsdAnyUri

from .parser import OpcOxml

NSMAP: Nsmap = {None: NAMESPACE_URI.MEDIA_TYPES_STREAM}


class OpcOxmlNSMediaTypesStream(OpcOxml, nsmap=NSMAP):
    pass


class CT_Types(OpcOxmlNSMediaTypesStream):
    @property
    def defaults(self) -> list[E_Default]:
        return self.all(E_Default)

    @property
    def overrides(self) -> list[E_Override]:
        return self.all(E_Override)


class CT_Default(OpcOxmlNSMediaTypesStream):
    Extension = AttrRequired("Extension", ST_Extension)
    ContentType = AttrRequired("ContentType", ST_ContentType)


class CT_Override(OpcOxmlNSMediaTypesStream):
    ContentType = AttrRequired("ContentType", ST_ContentType)
    PartName = AttrRequired("PartName", XsdAnyUri)


# -------------------- ELEMENTS --------------------


class E_Types(CT_Types, tag="Types"):
    pass


class E_Default(CT_Default, tag="Default"):
    pass


class E_Override(CT_Override, tag="Override"):
    pass
