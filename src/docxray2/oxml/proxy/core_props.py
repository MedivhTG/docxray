from datetime import datetime
from typing import Any

# docxray stuff
from docxray2.oxml.xml.core_properties import CT_CoreProperties, E_Category

from .base import DocxElementProxy


class CoreProperties(DocxElementProxy[CT_CoreProperties]):
    @property
    def category(self) -> str | None:
        return self._get_elm_content("category")

    @category.setter
    def category(self, value: str) -> None:
        category_elm = self.element.category
        if category_elm is None:
            category_elm = E_Category.new()
        category_elm.text = value

    @property
    def content_status(self) -> str | None:
        return self._get_elm_content("contentStatus")

    @property
    def created(self) -> datetime | None:
        return self._get_w3cdtf_elm_content("created")

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

    def _get_w3cdtf_elm_content(self, name: str) -> datetime | None:
        w3cdtf_elm = getattr(self.element, name)
        if w3cdtf_elm is None:
            return None
        # Call for validate
        _ = w3cdtf_elm.schemaType
        return w3cdtf_elm.content
