import re
from datetime import datetime
from typing import Any
from warnings import warn

# docxray stuff
from docxray2.opc.oxml.core_properties import (
    CT_CoreProperties,
    E_Category,
    E_ContentStatus,
    E_Keywords,
    E_LastModifiedBy,
    E_LastPrinted,
    E_Revision,
    E_Version,
)
from docxray2.opc.oxml.dublin_core import (
    E_Created,
    E_Creator,
    E_Description,
    E_Identifier,
    E_Language,
    E_Modified,
    E_Subject,
    E_Title,
)
from docxray2.opc.oxml.parser import OpcOxml
from docxray2.opc.proxy.base import OpcElementProxy
from docxray2.xsd.w3cdtf import W3CDTFDateTime

LANG_RFC3066_RE = re.compile(r"^[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*$")


class CoreProperties(OpcElementProxy[CT_CoreProperties]):
    """Core properties of a package as defined in ECMA-376 Part 2, Section 8.

    These properties provide a well-known set of metadata for packages,
    drawn from three sources:
      - Open Packaging Conventions (category, contentStatus, keywords,
        lastModifiedBy, lastPrinted, revision, version)
      - Dublin Core Metadata Element Set (creator, description, identifier,
        language, subject, title)
      - DCMI Metadata Terms (created, modified, as W3CDTF)

    See ECMA-376 Part 2, Table 3 for the authoritative mapping.
    """

    @property
    def category(self) -> str | None:
        """A categorization of the content of this package."""
        return self._get_elm_content("category")

    @category.setter
    def category(self, value: str) -> None:
        self._set_elm_content(E_Category, "category", value)

    @property
    def content_status(self) -> str | None:
        """The status of the content."""
        return self._get_elm_content("contentStatus")

    @content_status.setter
    def content_status(self, value: str) -> None:
        self._set_elm_content(E_ContentStatus, "contentStatus", value)

    @property
    def created(self) -> W3CDTFDateTime | None:
        """Date of creation of the resource."""
        return self._get_w3cdtf_elm_content("created")

    @created.setter
    def created(self, value: W3CDTFDateTime | datetime) -> None:
        self._set_elm_content(E_Created, "created", value)

    @property
    def creator(self) -> str | None:
        """An entity primarily responsible for making the content of the resource."""
        return self._get_elm_content("creator")

    @creator.setter
    def creator(self, value: str) -> None:
        self._set_elm_content(E_Creator, "creator", value)

    @property
    def description(self) -> str | None:
        """An explanation of the content of the resource."""
        return self._get_elm_content("description")

    @description.setter
    def description(self, value: str) -> None:
        self._set_elm_content(E_Description, "description", value)

    @property
    def identifier(self) -> str | None:
        """An unambiguous reference to the resource within a given context."""
        return self._get_elm_content("identifier")

    @identifier.setter
    def identifier(self, value: str) -> None:
        self._set_elm_content(E_Identifier, "identifier", value)

    @property
    def keywords(self) -> str | None:
        """A delimited set of keywords to support searching and indexing.
        This is typically a list of terms that are not available elsewhere in the properties.

        **NOTE:** Keywords canonicallly contained as one raw string,
        but sometimes element may contain subelements `<cp:value>`
        (as allowed in ECMA-376), but we will set them as in first way.
        """
        keywords_elm = self.element.keywords
        if keywords_elm is None:
            return None
        return keywords_elm.tag_full_content()

    @keywords.setter
    def keywords(self, value: str) -> None:
        keywords_elm = self.element.keywords
        if keywords_elm is None:
            keywords_elm = E_Keywords.new()
            keywords_elm.content = value
            self.element.append(keywords_elm)
        else:
            keywords_elm.clear()
            keywords_elm.content = value

    @property
    def language(self) -> str | None:
        """The language of the intellectual content of the resource.
        Note that IETF RFC 3066 provides guidance on encoding to
        represent languages."""
        return self._get_elm_content("language")

    @language.setter
    def language(self, value: str) -> None:
        if not LANG_RFC3066_RE.match(value):
            warn(
                f"Language tag {value!r} does not match the recommended "
                f"RFC 3066 / BCP 47 format. It will be stored as-is.",
                UserWarning,
                stacklevel=2,
            )
        self._set_elm_content(E_Language, "language", value)

    @property
    def last_modified_by(self) -> str | None:
        """The user who performed the last modification. The
        identification is environment-specific."""
        return self._get_elm_content("lastModifiedBy")

    @last_modified_by.setter
    def last_modified_by(self, value: str) -> None:
        self._set_elm_content(E_LastModifiedBy, "lastModifiedBy", value)

    @property
    def last_printed(self) -> W3CDTFDateTime | None:
        """The date and time of the last printing."""
        return self._get_elm_content("lastPrinted")

    @last_printed.setter
    def last_printed(self, value: W3CDTFDateTime | datetime) -> None:
        self._set_elm_content(E_LastPrinted, "lastPrinted", value)

    @property
    def modified(self) -> W3CDTFDateTime | None:
        """Date on which the resource was changed."""
        return self._get_w3cdtf_elm_content("modified")

    @modified.setter
    def modified(self, value: W3CDTFDateTime | datetime) -> None:
        self._set_elm_content(E_Modified, "modified", value)

    @property
    def revision(self) -> str | None:
        """The revision number."""
        return self._get_elm_content("revision")

    @revision.setter
    def revision(self, value: str) -> None:
        self._set_elm_content(E_Revision, "revision", value)

    @property
    def subject(self) -> str | None:
        """The topic of the content of the resource."""
        return self._get_elm_content("subject")

    @subject.setter
    def subject(self, value: str) -> None:
        self._set_elm_content(E_Subject, "subject", value)

    @property
    def title(self) -> str | None:
        """The name given to the resource."""
        return self._get_elm_content("title")

    @title.setter
    def title(self, value: str) -> None:
        self._set_elm_content(E_Title, "title", value)

    @property
    def version(self) -> str | None:
        """The version number."""
        return self._get_elm_content("version")

    @version.setter
    def version(self, value: str) -> None:
        self._set_elm_content(E_Version, "version", value)

    def _get_elm_content(self, name: str) -> Any | None:
        elm = getattr(self.element, name)
        if elm is None:
            return None
        return elm.content

    def _set_elm_content(
        self, elm_cls: type[OpcOxml], name: str, value: Any
    ) -> None:
        elm = getattr(self.element, name)
        if elm is None:
            elm = elm_cls.new()
            self.element.append(elm)
        elm.content = value  # pyright: ignore[reportAttributeAccessIssue]

    def _get_w3cdtf_elm_content(self, name: str) -> W3CDTFDateTime | None:
        w3cdtf_elm = getattr(self.element, name)
        if w3cdtf_elm is None:
            return None
        # Call to validate
        _ = w3cdtf_elm.schemaType
        return w3cdtf_elm.content
