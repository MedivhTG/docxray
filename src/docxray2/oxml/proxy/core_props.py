from datetime import datetime
from typing import Any

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.oxml.xml.core_properties import (
    CT_CoreProperties,
    E_Category,
    E_ContentStatus,
)
from docxray2.oxml.xml.dublin_core import E_Created

from .base import DocxElementProxy


class CoreProperties(DocxElementProxy[CT_CoreProperties]):
    @property
    def category(self) -> str | None:
        return self._get_elm_content("category")

    @category.setter
    def category(self, value: str) -> None:
        self._set_elm_content(E_Category, "category", value)

    @property
    def content_status(self) -> str | None:
        return self._get_elm_content("contentStatus")

    @content_status.setter
    def content_status(self, value: str) -> None:
        return self._set_elm_content(E_ContentStatus, "contentStatus", value)

    @property
    def created(self) -> datetime | None:
        return self._get_w3cdtf_elm_content("created")

    @created.setter
    def created(self, value: datetime) -> None:
        return self._set_elm_content(E_Created, "created", value)

    @property
    def creator(self) -> str | None:
        return self._get_elm_content("creator")

    @property
    def description(self) -> str | None:
        return self._get_elm_content("description")

    @property
    def identifier(self) -> str | None:
        return self._get_elm_content("identifier")

    @property
    def keywords(self) -> str | None:
        keywords_elm = self.element.keywords
        if keywords_elm is None:
            return None
        return keywords_elm.tag_full_content()

    @property
    def language(self) -> str | None:
        return self._get_elm_content("language")

    @property
    def last_modified_by(self) -> str | None:
        return self._get_elm_content("lastModifiedBy")

    @property
    def last_printed(self) -> datetime | None:
        return self._get_elm_content("lastPrinted")

    @property
    def modified(self) -> datetime | None:
        return self._get_w3cdtf_elm_content("modified")

    @property
    def revision(self) -> str | None:
        return self._get_elm_content("revision")

    @property
    def subject(self) -> str | None:
        return self._get_elm_content("subject")

    @property
    def title(self) -> str | None:
        return self._get_elm_content("title")

    @property
    def version(self) -> str | None:
        return self._get_elm_content("version")

    def _get_elm_content(self, name: str) -> Any | None:
        elm = getattr(self.element, name)
        if elm is None:
            return None
        return elm.content

    def _set_elm_content(
        self, elm_cls: type[Oxml], name: str, value: Any
    ) -> None:
        elm = getattr(self.element, name)
        if elm is None:
            elm = elm_cls.new()
            self.element.append(elm)
        elm.content = value  # pyright: ignore[reportAttributeAccessIssue]

    def _get_w3cdtf_elm_content(self, name: str) -> datetime | None:
        w3cdtf_elm = getattr(self.element, name)
        if w3cdtf_elm is None:
            return None
        # Call for validate
        _ = w3cdtf_elm.schemaType
        return w3cdtf_elm.content
