from __future__ import annotations

# docxray stuff
from docxray2.opc.xsd.relationships import ST_TargetMode
from docxray2.xmlchemy import AttrOptional, AttrRequired
from docxray2.xsd.primitives import XsdAnyUri, XsdID

from .parser import OpcOxml


class OpcOxmlNSRelationships(OpcOxml, ns="r"):
    pass


class CT_Relationships(OpcOxmlNSRelationships):
    @property
    def relationships(self) -> list[E_Relationship]:
        return self.zero_or_more(E_Relationship)


class CT_Relationship(OpcOxmlNSRelationships):
    TargetMode = AttrOptional("TargetMode", ST_TargetMode)
    Target = AttrRequired("Target", XsdAnyUri)
    Type = AttrRequired("Type", XsdAnyUri)
    Id = AttrRequired("Id", XsdID)


# -------------------- ELEMENTS --------------------


class E_Relationships(CT_Relationships, tag="Relationships"):
    pass


class E_Relationship(CT_Relationship, tag="Relationship"):
    pass
