from __future__ import annotations

from typing import TYPE_CHECKING, Any
from warnings import deprecated

from pydantic import BaseModel

# docxray stuff
from docxray2.oxml.parser import Oxml
from docxray2.oxml.shared_dpe import (
    E_Application,
    E_AppVersion,
    E_Characters,
    E_CharactersWithSpaces,
    E_Company,
    E_DigSig,
    E_DocSecurity,
    E_HeadingPairs,
    E_HiddenSlides,
    E_HyperlinkBase,
    E_HyperlinksChanged,
    E_Lines,
    E_LinksUpToDate,
    E_Manager,
    E_MMClips,
    E_Notes,
    E_Pages,
    E_Paragraphs,
    E_PresentationFormat,
    E_Properties,
    E_ScaleCrop,
    E_SharedDoc,
    E_Slides,
    E_Template,
    E_TitlesOfParts,
    E_TotalTime,
    E_Words,
)
from docxray2.oxml.shared_dpvt import (
    E_I1,
    E_I2,
    E_I4,
    E_I8,
    E_Blob,
    E_Bstr,
    E_Int,
    E_Lpstr,
    E_Lpwstr,
    E_Ui1,
    E_Ui2,
    E_Ui4,
    E_Ui8,
    E_Uint,
    E_Variant,
    E_Vector,
)
from docxray2.simple_types.enums import SE_VECTOR_BASE_TYPE

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

    @application_name.setter
    def application_name(self, value: str | None) -> None:
        self._set_content_elm(E_Application, "application", value)

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

    @application_version.setter
    def application_version(self, value: str | None) -> None:
        self._set_content_elm(E_AppVersion, "app_version", value)

    @property
    def total_number_of_characters(self) -> int | None:
        """Specifies the total number of characters in a document."""
        return self._get_elm_content("characters")

    @total_number_of_characters.setter
    def total_number_of_characters(self, value: int | None) -> None:
        self._set_content_elm(E_Characters, "characters", value)

    @property
    def number_of_characters_with_spaces(self) -> int | None:
        """Specifies the last count of the number of characters (including spaces) in this document."""
        return self._get_elm_content("characters_with_spaces")

    @number_of_characters_with_spaces.setter
    def number_of_characters_with_spaces(self, value: int | None) -> None:
        self._set_content_elm(
            E_CharactersWithSpaces, "characters_with_spaces", value
        )

    @property
    def name_of_company(self) -> str | None:
        """Specifies the name of a company associated with the document."""
        return self._get_elm_content("company")

    @name_of_company.setter
    def name_of_company(self, value: str | None) -> None:
        self._set_content_elm(E_Company, "company", value)

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

    @digital_signature.setter
    def digital_signature(self, value: bytes | None) -> None:
        dig_sig_elm = self.element.dig_sig
        if dig_sig_elm is None:
            if value is None:
                return
            blob_elm = E_Blob.new()
            blob_elm.content = value
            dig_sig_elm = E_DigSig.new()
            dig_sig_elm.append_child(blob_elm)
            self.element.append_child(dig_sig_elm)
            return
        if value is None:
            self.element.remove_child(dig_sig_elm)
        else:
            blob_elm = E_Blob.new()
            blob_elm.content = value
            dig_sig_elm.append_child(blob_elm)
            self.element.append_child(dig_sig_elm)

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

    @document_security.setter
    def document_security(
        self, value: WD_DOCUMENT_SECURITY | int | None
    ) -> None:
        if isinstance(value, int):
            value = WD_DOCUMENT_SECURITY.new(value)
        self._set_content_elm(E_DocSecurity, "doc_security", value)

    @property
    def heading_groups(self) -> list[HeadingGroup]:
        return HeadingGroup.from_elm(self.element)

    @heading_groups.setter
    def heading_groups(self, value: list[HeadingGroup]) -> None:
        hp_elm_old = self.element.heading_pairs
        top_elm_old = self.element.titles_of_parts
        # TitlesOfParts
        top_size = sum(len(hg.titles) for hg in value)
        top_vec_elm = None
        if top_size > 0:
            top_vec_elm = E_Vector.new()
            top_vec_elm.base_type = SE_VECTOR_BASE_TYPE.LPSTR
            top_vec_elm.size = top_size
            for hg in value:
                if not isinstance(hg, HeadingGroup):
                    raise TypeError(
                        f"Type mismatch for HeadingGroup, got: {type(hg)}"
                    )
                for title in hg.titles:
                    lpstr_elm = E_Lpstr.new()
                    lpstr_elm.content = title
                    top_vec_elm.append_child(lpstr_elm)
        top_elm_new = None
        if top_vec_elm is not None:
            top_elm_new = E_TitlesOfParts.new()
            top_elm_new.append_child(top_vec_elm)
        # HeadingPairs
        hp_size = 2 * len(value)
        hp_vec_elm = None
        if hp_size > 0:
            hp_vec_elm = E_Vector.new()
            hp_vec_elm.base_type = SE_VECTOR_BASE_TYPE.VARIANT
            hp_vec_elm.size = hp_size
            for hg in value:
                name_vec_elm = E_Variant.new()
                lpstr_elm = E_Lpstr.new()
                lpstr_elm.content = hg.name
                name_vec_elm.append_child(lpstr_elm)
                count_v = E_Variant.new()
                i4 = E_I4.new()
                i4.content = len(hg.titles)
                count_v.append_child(i4)
                hp_vec_elm.append_child(name_vec_elm)
                hp_vec_elm.append_child(count_v)
        hp_elm_new = None
        if hp_vec_elm is not None:
            hp_elm_new = E_HeadingPairs.new()
            hp_elm_new.append_child(hp_vec_elm)
        # Fallback on empty list
        if top_elm_new is None or hp_elm_new is None:
            if top_elm_old is not None:
                self.element.remove_child(top_elm_old)
            if hp_elm_old is not None:
                self.element.remove_child(hp_elm_old)
            return
        # Set elements (final)
        if top_elm_old is not None:
            self.element.replace_child(top_elm_old, top_elm_new)
        else:
            self.element.append_child(top_elm_new)
        if hp_elm_old is not None:
            self.element.replace_child(hp_elm_old, hp_elm_new)
        else:
            self.element.append_child(hp_elm_new)

    @property
    def number_of_hidden_slides(self) -> int | None:
        """Specifies the number of hidden slides in a presentation document."""
        return self._get_elm_content("hidden_slides")

    @number_of_hidden_slides.setter
    def number_of_hidden_slides(self, value: int | None) -> None:
        self._set_content_elm(E_HiddenSlides, "hidden_slides", value)

    # TODO: realize
    @property
    def hyperlink_list(self) -> None:
        """Specifies the set of hyperlinks that were in this document when last saved."""

    @property
    def relative_hyperlink_base(self) -> str | None:
        """Specifies the base string used for evaluating relative hyperlinks in this document.
        The possible"""
        return self._get_elm_content("hyperlink_base")

    @relative_hyperlink_base.setter
    def relative_hyperlink_base(self, value: str | None) -> None:
        self._set_content_elm(E_HyperlinkBase, "hyperlink_base", value)

    @property
    def hyperlinks_changed(self) -> bool | None:
        """Specifies that one or more hyperlinks in this part were updated exclusively in this part by a
        producer. The next producer to open this document shall update the hyperlink relationships with the new
        hyperlinks specified in this part."""
        return self._get_elm_content("hyperlinks_changed")

    @hyperlinks_changed.setter
    def hyperlinks_changed(self, value: bool | None) -> None:
        self._set_content_elm(E_HyperlinksChanged, "hyperlinks_changed", value)

    @property
    def number_of_lines(self) -> int | None:
        """Specifies the total number of lines in a document when last saved by a conforming producer if
        applicable."""
        return self._get_elm_content("lines")

    @number_of_lines.setter
    def number_of_lines(self, value: int | None) -> None:
        self._set_content_elm(E_Lines, "lines", value)

    @property
    def links_up_to_date(self) -> bool | None:
        """Indicates whether hyperlinks in a document are up-to-date. Set this property to TRUE to indicate
        that hyperlinks are updated. Set this property to FALSE to indicate that hyperlinks are outdated.
        """
        return self._get_elm_content("links_up_to_date")

    @links_up_to_date.setter
    def links_up_to_date(self, value: bool | None) -> None:
        self._set_content_elm(E_LinksUpToDate, "links_up_to_date", value)

    @property
    def manager(self) -> str | None:
        """Specifies the name of a supervisor associated with the document."""
        return self._get_elm_content("manager")

    @manager.setter
    def manager(self, value: str | None) -> None:
        self._set_content_elm(E_Manager, "manager", value)

    @property
    def total_number_of_multimedia_clips(self) -> int | None:
        """Specifies the total number of sound or video clips that are present in the document."""
        return self._get_elm_content("mm_clips")

    @total_number_of_multimedia_clips.setter
    def total_number_of_multimedia_clips(self, value: int | None) -> None:
        self._set_content_elm(E_MMClips, "mm_clips", value)

    @property
    def number_of_slides_containing_notes(self) -> int | None:
        """Specifies the number of slides in a presentation containing notes."""
        return self._get_elm_content("notes")

    @number_of_slides_containing_notes.setter
    def number_of_slides_containing_notes(self, value: int | None) -> None:
        self._set_content_elm(E_Notes, "notes", value)

    @property
    def total_number_of_pages(self) -> int | None:
        """Specifies the total number of pages of a document if applicable."""
        return self._get_elm_content("pages")

    @total_number_of_pages.setter
    def total_number_of_pages(self, value: int | None) -> None:
        self._set_content_elm(E_Pages, "pages", value)

    @property
    def total_number_of_paragraphs(self) -> int | None:
        """Specifies the total number of paragraphs found in a document if applicable."""
        return self._get_elm_content("paragraphs")

    @total_number_of_paragraphs.setter
    def total_number_of_paragraphs(self, value: int | None) -> None:
        self._set_content_elm(E_Paragraphs, "paragraphs", value)

    @property
    def intended_format_of_presentation(self) -> str | None:
        """Specifies the intended format for a presentation document. For example, a presentation intended
        to be shown on video has PresentationFormat "Video"."""
        return self._get_elm_content("presentation_format")

    @intended_format_of_presentation.setter
    def intended_format_of_presentation(self, value: str | None) -> None:
        self._set_content_elm(
            E_PresentationFormat, "presentation_format", value
        )

    @property
    def thumbnail_display_mode(self) -> bool | None:
        """Indicates the display mode of the document thumbnail. Set this property to TRUE to enable scaling
        of the document thumbnail to the display. Set this property to FALSE to enable cropping of the document
        thumbnail to show only sections that fits the display."""
        return self._get_elm_content("scale_crop")

    @thumbnail_display_mode.setter
    def thumbnail_display_mode(self, value: bool | None) -> None:
        self._set_content_elm(E_ScaleCrop, "scale_crop", value)

    @property
    def shared_document(self) -> bool | None:
        """Indicates if this document is currently shared between multiple producers. If this property is set to
        TRUE, producers should take care when updating the document."""
        return self._get_elm_content("shared_doc")

    @shared_document.setter
    def shared_document(self, value: bool | None) -> None:
        self._set_content_elm(E_SharedDoc, "shared_doc", value)

    @property
    def slides_metadata(self) -> int | None:
        """Specifies the total number of slides in a presentation document."""
        return self._get_elm_content("slides")

    @slides_metadata.setter
    def slides_metadata(self, value: int | None) -> None:
        self._set_content_elm(E_Slides, "slides", value)

    @property
    def name_of_document_template(self) -> str | None:
        """Specifies the name of an external document template containing format and style information
        used to create the current document."""
        return self._get_elm_content("template")

    @name_of_document_template.setter
    def name_of_document_template(self, value: str | None) -> None:
        self._set_content_elm(E_Template, "template", value)

    @property
    def total_edit_time_metadata(self) -> int | None:
        """Total time that a document has been edited. The default time unit is minutes."""
        return self._get_elm_content("total_time")

    @total_edit_time_metadata.setter
    def total_edit_time_metadata(self, value: int | None) -> None:
        self._set_content_elm(E_TotalTime, "total_time", value)

    @property
    def word_count(self) -> int | None:
        """Specifies the total number of words contained in a document when last saved."""
        return self._get_elm_content("words")

    @word_count.setter
    def word_count(self, value: int | None) -> None:
        self._set_content_elm(E_Words, "words", value)

    def _get_elm_content(self, name: str) -> Any | None:
        elm = getattr(self.element, name)
        if elm is None:
            return None
        return elm.content

    def _set_content_elm(
        self, elm_cls: type[Oxml], name: str, value: Any
    ) -> None:
        elm = getattr(self.element, name)
        if elm is None:
            if value is None:
                return
            elm = elm_cls.new()
            elm.content = value  # type: ignore[attr-defined]
            self.element.append_child(elm)
            return
        if value is None:
            self.element.remove_child(elm)
        else:
            elm.content = value  # pyright: ignore[reportAttributeAccessIssue]


class HeadingGroup(BaseModel):
    name: str
    titles: list[str]

    @classmethod
    def from_elm(cls, elm: E_Properties) -> list[HeadingGroup]:
        hp_elm = elm.heading_pairs
        if hp_elm is None:
            return []
        top_elm = elm.titles_of_parts
        if top_elm is None:
            raise ValueError("HeadingPairs present but TitlesOfParts missing")
        pairs = []
        vectors = hp_elm.vector.vectors
        if len(vectors) % 2 != 0:
            raise ValueError(
                "HeadingPairs vector must contain name/count pairs"
            )
        for name_vec, count_vec in zip(vectors[::2], vectors[1::2]):
            if not isinstance(name_vec, E_Variant) or not isinstance(
                count_vec, E_Variant
            ):
                raise TypeError(
                    f"Expected variants type in , got {type(name_vec)},{type(count_vec)}"
                )
            name_var = name_vec.variant
            count_var = count_vec.variant
            if not isinstance(name_var, (E_Lpstr, E_Lpwstr)):
                raise TypeError(
                    f"Expected lpstr/lpwstr in HeadingPairs, got {type(name_var)}"
                )
            if not isinstance(
                count_var,
                (
                    E_I1,
                    E_I2,
                    E_I4,
                    E_I8,
                    E_Int,
                    E_Ui1,
                    E_Ui2,
                    E_Ui4,
                    E_Ui8,
                    E_Uint,
                ),
            ):
                raise TypeError(
                    f"Expected integer variant in HeadingPairs, got {type(count_var)}"
                )
            htitle = name_var.content
            if not htitle:
                raise ValueError("HeadingPairs: empty group name")
            hcount = count_var.content
            if not isinstance(hcount, int):
                raise TypeError(
                    f"HeadingPairs: count for group `{htitle}` is missing or not an integer"
                )
            if hcount < 0:
                raise ValueError(
                    f"HeadingPairs: negative count for group `{hcount}`"
                )
            pairs.append((htitle, hcount))
        titles: list[str] = []
        for vector in top_elm.vector.vectors:
            if not isinstance(vector, (E_Lpstr, E_Lpwstr, E_Bstr)):
                raise TypeError(
                    f"Expected string variant in TitleOfParts, got {type[vector]}"
                )
            titles.append(vector.content or "")
        groups = []
        cursor = 0
        for name, count in pairs:
            chunk = titles[cursor : cursor + count]
            if len(chunk) != count:
                raise ValueError(
                    f"TitlesOfParts exhausted: group `{name}` claims {count} titles, "
                    f"only {len(chunk)} remain"
                )
            groups.append(HeadingGroup(name=name, titles=chunk))
            cursor += count
        return groups
