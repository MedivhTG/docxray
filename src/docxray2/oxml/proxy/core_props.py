from datetime import datetime
from typing import Any

# docxray stuff
from docxray2.oxml.xml.core_properties import CT_CoreProperties

from .base import DocxElementProxy
from .exceptions import DocxProxyInvalidOPCSchema

W3CDTF_VALID_SCHEMA = "dcterms:W3CDTF"


class CoreProperties(DocxElementProxy[CT_CoreProperties]):
    @property
    def category(self) -> str | None:
        return self._get_elm_content("category")

    @property
    def content_status(self) -> str | None:
        return self._get_elm_content("contentStatus")

    @property
    def created(self) -> datetime | None:
        created_elm = self.element.created
        if created_elm is None:
            return None
        schema = created_elm.schemaType
        if schema != W3CDTF_VALID_SCHEMA:
            raise DocxProxyInvalidOPCSchema(
                f"Invalid schema type {schema} for {created_elm.qname()}"
            )
        return created_elm.content

    @property
    def creator(self) -> str | None:
        return self._get_elm_content("creator")

    @property
    def description(self) -> str | None:
        return self._get_elm_content("description")

    @property
    def identifier(self) -> str | None:
        return self._get_elm_content("identifier")

    def _get_elm_content(self, name: str) -> Any | None:
        elm = getattr(self.element, name)
        if elm is None:
            return None
        return elm.content
