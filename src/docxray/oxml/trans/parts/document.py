"""|DocumentPart| and closely related objects."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.opc.constants import RELATIONSHIP_TYPE as RT
from docxray.oxml.trans.document import CT_Document
from docxray.oxml.trans.parts.numbering import NumberingPart
from docxray.oxml.trans.parts.settings import SettingsPart
from docxray.oxml.trans.parts.story import StoryPart
from docxray.oxml.trans.parts.styles import StylesPart
from docxray.oxml.trans.parts.theme import ThemePart
from docxray.oxml.trans.proxy.document import Document
from docxray.oxml.trans.proxy.numbering.numbering import Numbering
from docxray.oxml.trans.proxy.settings import Settings
from docxray.oxml.trans.proxy.styles.styles import Styles
from docxray.oxml.trans.proxy.theme import Theme
from docxray.transform.ruleset import RuleSet


class DocumentPart(StoryPart[CT_Document]):
    """Main document part of a WordprocessingML (WML) package, aka a .docx file."""

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

    @cached_property
    def numbering(self) -> Numbering | None:
        """`Numbering` instance with list properties, `None` if no such part."""
        if self.numbering_part is None:
            return None
        return self.numbering_part.numbering

    @cached_property
    def styles_part(self) -> StylesPart:
        """Instance of |StylesPart| for this document."""
        return self.part_related_by(RT.STYLES, StylesPart)

    @cached_property
    def styles(self) -> Styles:
        """A |Styles| object providing access to the styles in the styles part of this document."""
        return self.styles_part.styles

    @cached_property
    def settings_part(self) -> SettingsPart:
        """Instance of |SettingsPart| for this document."""
        return self.part_related_by(RT.SETTINGS, SettingsPart)

    @cached_property
    def settings(self) -> Settings:
        """A |Settings| object providing access to the settings in the settings part of this document."""
        return self.settings_part.settings

    @cached_property
    def theme_part(self) -> ThemePart:
        return self.part_related_by(RT.THEME, ThemePart)

    @cached_property
    def theme(self) -> Theme:
        return self.theme_part.theme

    @cached_property
    def _default_html_ruleset(self) -> RuleSet:
        """Default `RuleSet` instance with transform rules."""
        return RuleSet.html_default()
