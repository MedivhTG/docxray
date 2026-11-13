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
        """Specifies the name of the application that created this document."""
        return self._get_elm_content("application")

    @property
    def application_version(self) -> str | None:
        """Specifies the version of the application which produced this document.

        The content of this property shall be of the form XX.YYYY where X and Y represent numerical values, or the
        document shall be considered non-conformant.

        **Note**: The contents of this property do not represent absolute values, but rather qualify the contents of the
        `application_name` property to differentiate between different versions of the same producer. Applications should use
        this information in an informative manner only (as document metadata).
        """
        return self._get_elm_content("app_version")

    @property
    def total_number_of_characters(self) -> int | None:
        """Specifies the total number of characters in a document."""
        return self._get_elm_content("characters")

    @property
    def number_of_characters_with_spaces(self) -> int | None:
        """Specifies the last count of the number of characters (including spaces) in this document."""
        return self._get_elm_content("characters_with_spaces")

    @property
    def name_of_company(self) -> str | None:
        """Specifies the name of a company associated with the document."""
        return self._get_elm_content("company")

    @property
    @deprecated(
        "This property is a mechanism used by legacy documents to store the digital signature of its binary "
        "representation, and should be avoided in favor of the well-defined mechanism defined in Part 2 (OPC). Any use of this "
        "property should be for legacy compatibility only, and is application-defined."
    )
    def digital_signature(self) -> bytes | None:
        """Contains the signature of a digitally signed document."""
        dig_sig_elm = self.element.dig_sig
        if dig_sig_elm is None:
            return None
        return dig_sig_elm.blob.content

    @property
    def document_security(self) -> WD_DOCUMENT_SECURITY | None:
        """Specifies the security level of a document as a numeric value. Document security is
        defined as intflags:

        - 1 - Document is password protected
        - 2 - Document is recommended to be opened as read-only.
        - 4 - Document is enforced to be opened as read-only.
        - 8 - Document is locked for annotation.

        **NOTE**: Also Word/office-app may save document with zero value or other incompatible
        values with the specification that means none of security levels were applied. To get
        origin value get it as follows `extf_props.element.doc_security.content`.
        """
        content = self._get_elm_content("doc_security")
        if content is None:
            return None
        return WD_DOCUMENT_SECURITY.new(content)

    # TODO: realize
    @property
    def heading_pairs(self) -> None:
        """Heading pairs indicates the grouping of document parts and the number of parts in each group. These parts are
        not document parts but conceptual representations of document sections.
        """

    @property
    def number_of_hidden_slides(self) -> int | None:
        """Specifies the number of hidden slides in a presentation document."""
        return self._get_elm_content("hidden_slides")

    # TODO: realize
    @property
    def hyperlink_list(self) -> None:
        """Specifies the set of hyperlinks that were in this document when last saved."""

    @property
    def relative_hyperlink_base(self) -> str | None:
        """Specifies the base string used for evaluating relative hyperlinks in this document.
        The possible"""
        return self._get_elm_content("hyperlink_base")

    @property
    def hyperlinks_changed(self) -> bool | None:
        """Specifies that one or more hyperlinks in this part were updated exclusively in this part by a
        producer. The next producer to open this document shall update the hyperlink relationships with the new
        hyperlinks specified in this part."""
        return self._get_elm_content("hyperlinks_changed")

    @property
    def number_of_lines(self) -> int | None:
        """Specifies the total number of lines in a document when last saved by a conforming producer if
        applicable."""
        return self._get_elm_content("lines")

    @property
    def links_up_to_date(self) -> bool | None:
        """Indicates whether hyperlinks in a document are up-to-date. Set this property to TRUE to indicate
        that hyperlinks are updated. Set this property to FALSE to indicate that hyperlinks are outdated.
        """
        return self._get_elm_content("links_up_to_date")

    @property
    def manager(self) -> str | None:
        """Specifies the name of a supervisor associated with the document."""
        return self._get_elm_content("manager")

    @property
    def total_number_of_multimedia_clips(self) -> int | None:
        """Specifies the total number of sound or video clips that are present in the document."""
        return self._get_elm_content("mm_clips")

    @property
    def number_of_slides_containing_notes(self) -> int | None:
        """Specifies the number of slides in a presentation containing notes."""
        return self._get_elm_content("notes")

    @property
    def total_number_of_pages(self) -> int | None:
        """Specifies the total number of pages of a document if applicable."""
        return self._get_elm_content("pages")

    @property
    def total_number_of_paragraphs(self) -> int | None:
        """Specifies the total number of paragraphs found in a document if applicable."""
        return self._get_elm_content("paragraphs")

    @property
    def intended_format_of_presentation(self) -> str | None:
        """Specifies the intended format for a presentation document. For example, a presentation intended
        to be shown on video has PresentationFormat "Video"."""
        return self._get_elm_content("presentation_format")

    @property
    def thumbnail_display_mode(self) -> bool | None:
        """Indicates the display mode of the document thumbnail. Set this property to TRUE to enable scaling
        of the document thumbnail to the display. Set this property to FALSE to enable cropping of the document
        thumbnail to show only sections that fits the display."""
        return self._get_elm_content("scale_crop")

    @property
    def shared_document(self) -> bool | None:
        """Indicates if this document is currently shared between multiple producers. If this property is set to
        TRUE, producers should take care when updating the document."""
        return self._get_elm_content("shared_doc")

    @property
    def slides_metadata(self) -> int | None:
        """Specifies the total number of slides in a presentation document."""
        return self._get_elm_content("slides")

    @property
    def name_of_document_template(self) -> str | None:
        """Specifies the name of an external document template containing format and style information
        used to create the current document."""
        return self._get_elm_content("template")

    # TODO: realize
    @property
    def part_titles(self) -> None:
        """Specifies the title of each document. These parts are not document parts but conceptual
        representations of document sections."""

    @property
    def total_edit_time_metadata(self) -> int | None:
        """Total time that a document has been edited. The default time unit is minutes."""
        return self._get_elm_content("total_time")

    @property
    def word_count(self) -> int | None:
        """Specifies the total number of words contained in a document when last saved."""
        return self._get_elm_content("words")

    def _get_elm_content(self, name: str) -> Any | None:
        elm = getattr(self.element, name)
        if elm is None:
            return None
        return elm.content
