"""|DocumentPart| and closely related objects."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.document import Document
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.oxml.document import CT_Document
from docxray.parts.numbering import NumberingPart
from docxray.parts.story import StoryPart
from docxray.parts.styles import StylesPart
from docxray.styles.styles import Styles


class DocumentPart(StoryPart[CT_Document]):
    """Main document part of a WordprocessingML (WML) package, aka a .docx file.

    Acts as broker to other parts such as image, core properties, and style parts. It
    also acts as a convenient delegate when a mid-document object needs a service
    involving a remote ancestor. The `Parented.part` property inherited by many content
    objects provides access to this part object for that purpose.
    """

    @cached_property
    def document(self) -> Document:
        """A |Document| object providing access to the content of this document."""
        return Document(self._element, self)

    @cached_property
    def numbering_part(self) -> NumberingPart | None:
        """A |NumberingPart| object providing access to the numbering definitions for this document."""
        try:
            return self.part_related_by(RT.NUMBERING, NumberingPart)
        except KeyError:
            return None

    @property
    def styles(self) -> Styles:
        """A |Styles| object providing access to the styles in the styles part of this
        document."""
        return self.styles_part.styles

    @cached_property
    def styles_part(self) -> StylesPart:
        """Instance of |StylesPart| for this document.

        Creates an empty styles part if one is not present.
        """
        return self.part_related_by(RT.STYLES, StylesPart)
