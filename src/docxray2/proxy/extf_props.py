from typing import TYPE_CHECKING, Any
from warnings import deprecated

# docxray stuff
from docxray2.oxml.shared_dpe import E_Properties

from .base import DocxElementProxy
from .enums import WD_DOCUMENT_SECURITY

if TYPE_CHECKING:

    # docxray stuff
    from docxray2.parts.extended_file_properties import (  # noqa: F401
        ExtendedFilePropertiesPart,
    )


# TODO: add other getters, add setters
class ExtentedFileProperties(
    DocxElementProxy[E_Properties, "ExtendedFilePropertiesPart"]
):
    @property
    def application_name(self) -> str | None:
        return self._get_elm_content("application")

    @property
    def application_version(self) -> str | None:
        return self._get_elm_content("app_version")

    @property
    def total_number_of_characters(self) -> int | None:
        return self._get_elm_content("characters")

    @property
    def number_of_characters_with_spaces(self) -> int | None:
        return self._get_elm_content("characters_with_spaces")

    @property
    def name_of_company(self) -> str | None:
        return self._get_elm_content("company")

    @property
    @deprecated(
        "It is a legacy mechanism. Use OPC signatures (Part 2) instead."
    )
    def digital_signature(self) -> bytes | None:
        dig_sig_elm = self.element.dig_sig
        if dig_sig_elm is None:
            return None
        return dig_sig_elm.blob.content

    @property
    def document_security(self) -> WD_DOCUMENT_SECURITY | None:
        content = self._get_elm_content("doc_security")
        if content is None:
            return None
        return WD_DOCUMENT_SECURITY.new(content)

    # TODO: realize
    @property
    def heading_pairs(self) -> None:
        pass

    @property
    def number_of_hidden_slides(self) -> int | None:
        return self._get_elm_content("hidden_slides")

    # TODO: realize
    @property
    def hyperlink_list(self) -> None:
        pass

    @property
    def relative_hyperlink_base(self) -> str | None:
        return self._get_elm_content("hyperlink_base")

    @property
    def hyperlinks_changed(self) -> bool | None:
        return self._get_elm_content("hyperlinks_changed")

    @property
    def number_of_lines(self) -> int | None:
        return self._get_elm_content("lines")

    @property
    def links_up_to_date(self) -> bool | None:
        return self._get_elm_content("links_up_to_date")

    @property
    def manager(self) -> str | None:
        return self._get_elm_content("manager")

    @property
    def total_number_of_multimedia_clips(self) -> int | None:
        return self._get_elm_content("mm_clips")

    @property
    def number_of_slides_containing_notes(self) -> int | None:
        return self._get_elm_content("notes")

    @property
    def total_number_of_pages(self) -> int | None:
        return self._get_elm_content("pages")

    @property
    def total_number_of_paragraphs(self) -> int | None:
        return self._get_elm_content("paragraphs")

    @property
    def intended_format_of_presentation(self) -> str | None:
        return self._get_elm_content("presentation_format")

    def _get_elm_content(self, name: str) -> Any | None:
        elm = getattr(self.element, name)
        if elm is None:
            return None
        return elm.content
