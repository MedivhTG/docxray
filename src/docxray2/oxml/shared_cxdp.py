from __future__ import annotations

# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.oxml.parser import Oxml
from docxray2.simple_types.shared_cst import ST_Guid
from docxray2.xmlchemy import AttrRequired, Nsmap
from docxray2.xsd.primitives import XsdString

NSMAP: Nsmap = {"ds": NAMESPACE.CUSTOM_XML}


class OxmlNSCustomXmlDataProperties(Oxml, ns="ds", nsmap=NSMAP):
    pass


class CT_DatastoreSchemaRef(OxmlNSCustomXmlDataProperties):
    uri = AttrRequired("uri", XsdString[str])


class CT_DatastoreSchemaRefs(OxmlNSCustomXmlDataProperties):
    @property
    def schema_refs(self) -> list[E_SchemaRef]:
        return self.all(E_SchemaRef)


class CT_DatastoreItem(OxmlNSCustomXmlDataProperties):
    item_id = AttrRequired("ds:itemID", ST_Guid)

    @property
    def schema_refs(self) -> E_SchemaRefs | None:
        return self.one_or_none(E_SchemaRefs)


# -------------------- ELEMENTS --------------------


class E_DatastoreItem(CT_DatastoreItem, tag="datastoreItem"):
    pass


class E_SchemaRef(CT_DatastoreSchemaRef, tag="schemaRef"):
    pass


class E_SchemaRefs(CT_DatastoreSchemaRefs, tag="schemaRefs"):
    pass
