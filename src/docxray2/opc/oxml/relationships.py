from __future__ import annotations

# docxray stuff
from docxray2.ns import NAMESPACE_URI
from docxray2.opc.xsd.relationships import ST_TargetMode
from docxray2.xmlchemy import AttrOptional, AttrRequired, Nsmap
from docxray2.xsd.primitives import XsdAnyUri, XsdID

from .parser import OpcOxml

NSMAP: Nsmap = {None: NAMESPACE_URI.RELATIONSHIPS}


class OpcOxmlNSRelationships(OpcOxml, nsmap=NSMAP):
    pass


class CT_Relationships(OpcOxmlNSRelationships):
    @property
    def relationships(self) -> list[E_Relationship]:
        return self.all(E_Relationship)


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
