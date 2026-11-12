from __future__ import annotations

from typing import Self

# docxray stuff
from docxray2.ns import NAMESPACE_URI
from docxray2.opc.xsd.content_types import ST_ContentType, ST_Extension
from docxray2.xmlchemy import AttrRequired
from docxray2.xsd.primitives import XsdAnyUri

from .parser import OpcOxml


class OpcOxmlNSMediaTypesStream(OpcOxml, ns="ct"):
    pass


class CT_Types(OpcOxmlNSMediaTypesStream):
    @property
    def defaults(self) -> list[E_Default]:
        return self.zero_or_more(E_Default)

    @property
    def overrides(self) -> list[E_Override]:
        return self.zero_or_more(E_Override)


class CT_Default(OpcOxmlNSMediaTypesStream):
    Extension = AttrRequired("Extension", ST_Extension)
    ContentType = AttrRequired("ContentType", ST_ContentType)


class CT_Override(OpcOxmlNSMediaTypesStream):
    ContentType = AttrRequired("ContentType", ST_ContentType)
    PartName = AttrRequired("PartName", XsdAnyUri)


# -------------------- ELEMENTS --------------------


class E_Types(CT_Types, tag="Types"):
    @classmethod
    def new(
        cls,
        exclude_tag_prefix: bool = True,
        nsmap: dict[str | None, str] | None = None,
    ) -> Self:
        # To create with xmlns="http://schemas.openxmlformats.org/package/2006/content-types"
        nsmap = {None: NAMESPACE_URI.MEDIA_TYPES_STREAM}
        return super().new(exclude_tag_prefix, nsmap)


class E_Default(CT_Default, tag="Default"):
    pass


class E_Override(CT_Override, tag="Override"):
    pass
