from __future__ import annotations

import warnings
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, TypedDict, cast

# docxray stuff
from docxray.colorize import Colorize
from docxray.length import Length
from docxray.oxml.t.proxy.base import (
    NotFound,
    from_doc_dflts,
    from_style_inheritance,
)
from docxray.oxml.t.proxy.compute import (
    hps_measure,
    on_off,
    signed_hps_measure,
    signed_twips_measure,
    text_scale,
)
from docxray.oxml.t.proxy.exceptions import DisplayError
from docxray.oxml.t.proxy.text.font import Font
from docxray.oxml.t.proxy.text.language import Language
from docxray.oxml.t.st.enums import (
    SE_HEX_COLOR_AUTO,
    SE_HIGHLIGHT_COLOR,
    SE_TEXT_EFFECT,
    SE_THEME_COLOR,
    SE_UNDERLINE,
    SE_VERTICAL_ALIGN_RUN,
)

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.t.proxy.numbering.numbering import Level

    from .run import Run

type FontVariant = Literal["caps", "small_caps"]
type StrikeLine = Literal["single", "double"]
type ReliefEffect = Literal["outline", "emboss", "imprint"]


class UnderlineInfo(TypedDict):
    line: SE_UNDERLINE
    color: str


class CharacterFormat:
    def __init__(self, char_proxy: Run | Level) -> None:
        from .run import Run

        self._proxy = char_proxy
        self._display = (
            self._display_run
            if isinstance(char_proxy, Run)
            else self._display_level
        )
        self._display_toggled = (
            self._display_run_toggled
            if isinstance(char_proxy, Run)
            else self._display_level_toggled
        )

    @cached_property
    def italic(self) -> bool:
        """
        Specifies whether the italic property should be applied to all characters in the contents of this run when displayed.

        This property is a toggle property. For complex script characters (Arabic, Hebrew, etc.), the iCs property is used instead.
        The distinction between complex and non-complex script is determined by the Unicode character values and the cs property.
        When this property is toggled on, the text is rendered in an italic (slanted) typeface. When toggled off, the text is
        rendered in a normal (upright) typeface.

        Rendering: Characters are displayed in italic/slanted typeface when True.
        Returns:
            bool: True if italics are applied, False otherwise.
        """
        if self._complex_script:
            return self._iCs
        return self._i

    @cached_property
    def bold(self) -> bool:
        """
        Specifies whether the bold property shall be applied to all characters in the contents of this run when displayed.

        This property is a toggle property. For complex script characters (Arabic, Hebrew, etc.), the bCs property is used instead.
        The distinction between complex and non-complex script is determined by the Unicode character values and the cs property.
        When this property is toggled on, the text is rendered with a heavier (bold) typeface. When toggled off, the text is
        rendered with a normal (regular) typeface.

        Rendering: Characters are displayed with heavier/bold typeface when True.
        Returns:
            bool: True if bold is applied, False otherwise.
        """
        if self._complex_script:
            return self._bCs
        return self._b

    @cached_property
    def font_size(self) -> Length | None:
        """
        Specifies the font size which shall be applied to all characters in the contents of this run when displayed.

        For complex script characters (Arabic, Hebrew, etc.), the szCs property is used instead. The distinction between
        complex and non-complex script is determined by the Unicode character values and the cs property.
        The font size controls the height of the characters. Larger values produce larger text, smaller values produce smaller text.

        Units: Half-points (1/144 of an inch). A value of 24 represents 12 points (1 point = 1/72 inch).

        Rendering: Controls the character height. Larger values = larger text, smaller values = smaller text.

        Returns:
            Length | None: Font size as Length object, or None if not specified.
        """
        if self._complex_script:
            return self._szCs
        return self._sz

    @cached_property
    def font_variant(self) -> FontVariant | None:
        """
        Specifies text transformation formatting applied to the run content.

        This property controls how letter case is displayed without changing the underlying Unicode characters.
        Two variants are available:
        - caps: All lowercase characters are displayed as capital letters. Non-alphabetic characters are unaffected.
          This does not change the Unicode characters, only the display method.
        - small_caps: All lowercase characters are displayed as capital letters in a font size two points smaller
          than the actual font size. Non-alphabetic characters are unaffected.
          This does not change the Unicode characters, only the display method.

        These two properties are mutually exclusive and cannot be applied simultaneously.

        Units: Enumeration (caps or small_caps).

        Rendering: Transforms the visual appearance of text characters without changing underlying character codes.

        Caps: "Hello" → "HELLO", Small Caps: "Hello" → "Hᴇʟʟᴏ" with smaller capital letters.

        Returns:
            FontVariant | None: 'caps' for all capitals, 'small_caps' for small capitals, or None if not applied.

        Raises:
            DisplayError: If both caps and small_caps are specified (mutually exclusive).
        """
        if self._caps and self._small_caps:
            raise DisplayError(
                "Mentiond 2 cases (caps, small_caps) when they are mutually exclusive"
            )
        if self._caps:
            return "caps"
        if self._small_caps:
            return "small_caps"
        return None

    @cached_property
    def strike_line(self) -> StrikeLine | None:
        """
        Specifies strikethrough formatting applied to the run content.

        This property draws one or two horizontal lines through the text characters. Two styles are available:
        - single: A single horizontal line through the center of each character.
        - double: Two horizontal lines through each character.

        These two properties are mutually exclusive and cannot be applied simultaneously.

        Units: Enumeration (single or double).

        Rendering: Draws one or two horizontal lines through the text characters.

        Returns:
            StrikeLine | None: 'single' for single strikethrough, 'double' for double strikethrough, or None if not applied.

        Raises:
            DisplayError: If both single and double strike are specified (mutually exclusive).
        """
        if self._single_strike and self._double_strike:
            raise DisplayError(
                "Mentiond 2 cases (single, double) when they are mutually exclusive"
            )
        if self._single_strike:
            return "single"
        if self._double_strike:
            return "double"
        return None

    @cached_property
    def underline_info(self) -> UnderlineInfo | None:
        """
        Specifies underline formatting applied to the run content.

        The underline appears directly below the character height (less all spacing above and below the characters on the line).
        The color can be specified directly as a hex value, set to 'auto' for automatic selection, or inherited from theme colors
        with optional tint/shade adjustments.

        Units:
            - line: Enumeration (SE_UNDERLINE).
            - color: Hex color string (e.g., '#FF0000') or 'auto'.

        Rendering: Draws a line beneath the text characters using the specified style and color.

        Returns:
            UnderlineInfo | None: Dictionary with 'line' and 'color' keys, or None if no underline is applied.
        """
        if self._u_line is None:
            return None
        return {
            "line": self._u_line,
            "color": Colorize.colorize(
                self._u_color or SE_HEX_COLOR_AUTO.AUTO,
                self._u_theme_color,
                self._proxy.document_part.theme.palette,
                self._u_theme_tint,
                self._u_theme_shade,
                prefer_theme=True,
            ),
        }

    @cached_property
    def vertical_alignment(self) -> SE_VERTICAL_ALIGN_RUN | None:
        """
        Specifies the vertical alignment applied to the contents of this run.

        This allows text to be repositioned as subscript or superscript without altering the font size.
        The text is rendered in a smaller size and positioned above (superscript) or below (subscript) the baseline.

        Units: Enumeration (SE_VERTICAL_ALIGN_RUN).
            - SUPERSCRIPT: Text is raised above the baseline and rendered in a smaller size.
            - SUBSCRIPT: Text is lowered below the baseline and rendered in a smaller size.
            - BASELINE: Text is positioned at the normal baseline (equivalent to no alignment).

        Rendering: Positions text above (superscript) or below (subscript) the baseline of surrounding text.

        Returns:
            SE_VERTICAL_ALIGN_RUN | None: SUPERSCRIPT, SUBSCRIPT, or None if baseline alignment.
        """
        align = self._display("rPr.vertAlign.val", False)
        if (
            isinstance(align, NotFound)
            or align == SE_VERTICAL_ALIGN_RUN.BASELINE
        ):
            return None
        return align

    @cached_property
    def font(self) -> Font | None:
        """
        Specifies the fonts which shall be used to display the text contents of this run.

        A single run can use up to four different font slots based on Unicode character classification:
        - ASCII (U+0000–U+007F): Basic Latin characters.
        - High ANSI: Latin Extended, Greek, Cyrillic, and other non-Asian scripts.
        - Complex Script: Arabic, Hebrew, Syriac, Thaana, and other bidirectional scripts.
        - East Asian: CJK (Chinese, Japanese, Korean) characters.

        The appropriate font is selected based on the Unicode character values and the cs/rtl properties.
        Theme fonts can be used to centrally manage font information across the document.

        Units: Font names (strings) or theme font references.

        Rendering: Determines the typeface used to render each character based on its Unicode script classification.

        Returns:
            Font | None: Font object containing all font slot specifications, or None if not specified.
        """
        rFonts_elm = self._display("rPr.rFonts")
        if isinstance(rFonts_elm, NotFound):
            return None
        return Font(rFonts_elm, self._proxy)

    @cached_property
    def language(self) -> Language | None:
        """
        Specifies the languages which shall be used to check spelling and grammar for the contents of this run.

        Different languages can be specified for three character types:
        - Latin characters (val): For Western scripts.
        - East Asian characters (eastAsia): For CJK scripts.
        - Complex Script characters (bidi): For right-to-left scripts like Arabic and Hebrew.

        This property affects spell-checking and grammar-checking behavior when the document is processed.

        Units: Language tags (e.g., 'en-US', 'fr-CA', 'he-IL', 'zh-CN').

        Rendering: Does not affect visual rendering, but influences spell-checking and grammar-checking behavior.

        Returns:
            Language | None: Language object containing language specifications, or None if not specified.
        """
        lang_elm = self._display("rPr.lang")
        if isinstance(lang_elm, NotFound):
            return None
        return Language(lang_elm, self._proxy)

    @cached_property
    def right_to_left(self) -> bool:
        """
        Specifies whether the contents of this run shall have right-to-left characteristics.

        When this property is applied:
        - All characters are treated as complex script for formatting purposes (uses bCs, iCs, szCs, etc.).
        - Acts as a right-to-left override for weak and neutral character types in the Unicode Bidirectional Algorithm.
        - Affects the bidirectional algorithm for text layout and reordering.

        This property provides higher-level information beyond what is implicitly derived from the Unicode Bidirectional algorithm.

        Units: Boolean (True/False).

        Rendering: Text is displayed right-to-left, affecting both character formatting selection and text directionality.

        Returns:
            bool: True if right-to-left characteristics are applied, False otherwise.
        """
        return on_off(self._display("rPr.rtl.val", True))

    @cached_property
    def color(self) -> str:
        """Specifies the color which shall be used to display the contents of this run.

        The color can be explicitly specified as a hex value, set to 'auto' for automatic selection (consumer chooses
        appropriate color based on background), or inherited from theme colors with optional tint/shade adjustments.
        Theme colors allow for centralized color management across the document.

        Units: Hex color string (RRGGBB format) or 'auto'.

        Rendering: Determines the text color used when rendering the run contents.

        Returns:
            str: Color string in hex format (e.g., '#FF0000' for red) or 'auto'.
        """
        return Colorize.colorize(
            self._color or SE_HEX_COLOR_AUTO.AUTO,
            self._theme_color,
            self._proxy.document_part.theme.palette,
            self._theme_tint,
            self._theme_shade,
            prefer_theme=True,
        )

    @cached_property
    def highlight(self) -> SE_HIGHLIGHT_COLOR | None:
        """Specifies a highlighting color which is applied as a background behind the contents of this run.

        Highlighting is typically used for marking or emphasizing text. If run shading (shd) is also specified,
        the highlighting color supersedes the shading for the contents of the run.

        Units: Enumeration (SE_HIGHLIGHT_COLOR) - predefined highlight colors (yellow, red, green, etc.).

        Rendering: Draws a colored background behind the text characters, overriding any shading that may be present.

        Returns:
            SE_HIGHLIGHT_COLOR | None: Highlight color enum, or None if no highlighting is applied.
        """
        highlight = self._display("rPr.highlight.val")
        if isinstance(highlight, NotFound):
            return None
        return highlight

    @cached_property
    def hide(self) -> bool:
        """Specifies whether the contents of this run shall be hidden from display.

        When hidden, the text is not rendered and does not occupy display space. The text content remains in the document
        but is invisible. Note that applications may have settings to force hidden text to be displayed.

        Rendering: When True, the text is not displayed and does not take up space in the layout.

        Returns:
            bool: True if text is hidden, False otherwise.
        """
        return self._display_toggled("rPr.vanish.val")

    @cached_property
    def horizontal_scale(self) -> int:
        """Specifies the percentage by which each character shall be expanded or compressed.

        This property scales the width of each character glyph, affecting the character's width without changing its height.
        Unlike letter_spacing, this property scales the actual character shapes rather than adding space between characters.
        Values greater than 100% expand characters horizontally, values less than 100% compress them.

        Units: Percentage (100% = normal width, 200% = double width, 50% = half width).

        Rendering: Stretches or compresses each character horizontally.

        Returns:
            int: Text scale percentage (default 100%).
        """
        scale = self._display("rPr.w.val")
        if isinstance(scale, NotFound):
            return 100
        return text_scale(scale)

    @cached_property
    def letter_spacing(self) -> Length | None:
        """Specifies the amount of character pitch which shall be added or removed after each character.

        This property adds or removes space between characters without changing the width of the actual characters.
        Unlike text_scale, this property adjusts spacing between characters rather than scaling the characters themselves.
        Positive values spread characters apart, negative values bring them closer together.

        Units: Twentieths of a point (1/1440th of an inch). Positive values add space, negative values reduce space.

        Rendering: Increases or decreases the horizontal space between characters.

        Returns:
            Length | None: Length object representing spacing, or None if not specified.
        """
        spacing = self._display("rPr.spacing.val")
        if isinstance(spacing, NotFound):
            return None
        return signed_twips_measure(spacing)

    @cached_property
    def vertical_offset(self) -> Length | None:
        """Specifies the amount by which text shall be raised or lowered for this run.

        This property allows text to be repositioned vertically without altering the font size.
        Positive values raise the text above the baseline of surrounding text, negative values lower it below the baseline.

        Units: Half-points (1/144 of an inch). Positive values raise text, negative values lower text.

        Rendering: Positions text above (positive value) or below (negative value) the baseline of surrounding text.

        Returns:
            Length | None: Length object representing offset, or None if not specified.
        """
        pos = self._display("rPr.position.val")
        if isinstance(pos, NotFound):
            return None
        return signed_hps_measure(pos)

    @cached_property
    def font_kerning(self) -> Length | None:
        """Specifies whether font kerning shall be applied to the contents of this run.

        Kerning automatically adjusts the spacing between specific character pairs to improve visual appearance
        (e.g., 'WA', 'To', 'AV'). The value specifies the smallest font size at which kerning should be applied.
        If the font size is smaller than this threshold, no kerning is performed.

        Units: Half-points (1/144 of an inch). Kerning is only applied if the font size is at least this value.

        Rendering: Automatically adjusts horizontal spacing between specific character pairs for improved appearance.

        Returns:
            Length | None: Length object representing kerning threshold, or None if not specified.
        """
        kern = self._display("rPr.kern.val")
        if isinstance(kern, NotFound):
            return None
        return hps_measure(kern)

    @property
    @warnings.deprecated("Not used in Word since app version `Word 2013`.")
    def relief_effect(self) -> ReliefEffect | None:
        """[DEPRECATED - Not used in Word since version 2013]

        Specifies a relief effect applied to the run content.

        These effects create three-dimensional appearances for text characters. Three styles are available:
        - outline: Displays characters with a one-pixel wide border around each glyph, creating a hollow appearance.
        - emboss: Displays characters as if raised off the page in relief (3D raised effect).
        - imprint: Displays characters as if pressed into the page (engraved effect).

        These three properties are mutually exclusive and cannot be applied simultaneously.

        Units: Enumeration (outline, emboss, or imprint).

        Rendering: Creates three-dimensional effects on text characters.

        Returns:
            ReliefEffect | None: 'outline', 'emboss', 'imprint', or None if not applied.

        Raises:
            DisplayError: If multiple relief effects are specified (mutually exclusive).
        """
        count = sum((self._outline, self._emboss, self._imprint))
        if count > 1:
            raise DisplayError(
                "Mentiond 3 cases (outline, emboss, imprint) when they are mutually exclusive"
            )
        if self._outline:
            return "outline"
        if self._emboss:
            return "emboss"
        if self._imprint:
            return "imprint"
        return None

    @property
    @warnings.deprecated("Not used in Word since app version `Word 2013`.")
    def shadow(self) -> bool:
        """[DEPRECATED - Not used in Word since version 2013]

        Specifies that the contents of this run shall be displayed with a shadow.

        For left-to-right text, the shadow appears beneath the text and to its right.
        For right-to-left text, the shadow appears beneath the text and to its left.

        Rendering: Draws a shadow offset from the text characters.

        Returns:
            bool: True if shadow is applied, False otherwise.
        """
        return self._shadow

    @property
    @warnings.deprecated("Not used in Word since app version `Word 2013`.")
    def animated_effect(self) -> SE_TEXT_EFFECT | None:
        """
        [DEPRECATED - Not used in Word since version 2013]
        Specifies an animated text effect which should be displayed when rendering the contents of this run.

        Animated effects include blinking, marching ants, sparkle text, and other visual animations.
        The effect is rendered around the extents of the text in the run.

        Returns:
            SE_TEXT_EFFECT | None: Animation effect enum, or None if no animation is applied.
            Units: Enumeration (SE_TEXT_EFFECT) - predefined animation types.
            Rendering: Creates animated effects (flashing, marching ants, etc.) around the text.
        """
        return self._effect

    @cached_property
    def _effect(self) -> SE_TEXT_EFFECT | None:
        effect = self._display("rPr.effect.val")
        if isinstance(effect, NotFound):
            return None
        return effect

    @cached_property
    def _shadow(self) -> bool:
        return self._display_toggled("rPr.shadow.val")

    @cached_property
    def _outline(self) -> bool:
        return self._display_toggled("rPr.outline.val")

    @cached_property
    def _emboss(self) -> bool:
        return self._display_toggled("rPr.emboss.val")

    @cached_property
    def _imprint(self) -> bool:
        return self._display_toggled("rPr.imprint.val")

    @cached_property
    def _sz(self) -> Length | None:
        size = self._display("rPr.sz.val")
        if isinstance(size, NotFound):
            return None
        return hps_measure(size)

    @cached_property
    def _szCs(self) -> Length | None:
        size = self._display("rPr.szCs.val")
        if isinstance(size, NotFound):
            return None
        return hps_measure(size)

    @cached_property
    def _i(self) -> bool:
        return self._display_toggled("rPr.i.val")

    @cached_property
    def _iCs(self) -> bool:
        return self._display_toggled("rPr.iCs.val")

    @cached_property
    def _b(self) -> bool:
        return self._display_toggled("rPr.b.val")

    @cached_property
    def _bCs(self) -> bool:
        return self._display_toggled("rPr.bCs.val")

    @cached_property
    def _complex_script(self) -> bool:
        """Spelling for text is complex (has arabic, chinese, etc. chars)."""
        return on_off(self._display("rPr.cs.val", True))

    @cached_property
    def _caps(self) -> bool:
        return self._display_toggled("rPr.caps.val")

    @cached_property
    def _small_caps(self) -> bool:
        return self._display_toggled("rPr.smallCaps.val")

    @cached_property
    def _single_strike(self) -> bool:
        return self._display_toggled("rPr.strike.val")

    @cached_property
    def _double_strike(self) -> bool:
        return on_off(self._display("rPr.dstrike.val", True))

    @cached_property
    def _u_line(self) -> SE_UNDERLINE | None:
        line = self._display("rPr.u.val", True)
        if isinstance(line, NotFound) or line == SE_UNDERLINE.NONE:
            return None
        if line is None:
            return SE_UNDERLINE.SINGLE
        return line

    @cached_property
    def _u_color(self) -> SE_HEX_COLOR_AUTO | bytes | None:
        color = self._display("rPr.u.color")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _u_theme_color(self) -> SE_THEME_COLOR | None:
        color = self._display("rPr.u.themeColor")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _u_theme_tint(self) -> bytes | None:
        tint = self._display("rPr.u.themeTint")
        if isinstance(tint, NotFound):
            return None
        return tint

    @cached_property
    def _u_theme_shade(self) -> bytes | None:
        shade = self._display("rPr.u.themeShade")
        if isinstance(shade, NotFound):
            return None
        return shade

    @cached_property
    def _color(self) -> SE_HEX_COLOR_AUTO | bytes | None:
        color = self._display("rPr.color.val")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _theme_color(self) -> SE_THEME_COLOR | None:
        color = self._display("rPr.color.themeColor")
        if isinstance(color, NotFound):
            return None
        return color

    @cached_property
    def _theme_tint(self) -> bytes | None:
        tint = self._display("rPr.color.themeTint")
        if isinstance(tint, NotFound):
            return None
        return tint

    @cached_property
    def _theme_shade(self) -> bytes | None:
        shade = self._display("rPr.color.themeShade")
        if isinstance(shade, NotFound):
            return None
        return shade

    def _display_level(self, path: str, optional: bool = False) -> Any:
        prop = self._proxy.prop(path, optional)
        if isinstance(prop, NotFound):
            return from_doc_dflts(self._proxy, path, optional)
        return prop

    def _display_level_toggled(self, path: str) -> bool:
        return on_off(self._display_level(path, True))

    def _display_run(self, path: str, optional: bool = False) -> Any:
        run = cast("Run", self._proxy)
        char_val = self._prop_run(path, optional, "both")
        if not isinstance(char_val, NotFound):
            return char_val
        para_val = run.paragraph._prop(path, optional, "paragraph-style")
        if not isinstance(para_val, NotFound):
            return para_val
        tbl_val = run.paragraph._prop(path, optional, "table-style")
        if not isinstance(tbl_val, NotFound):
            return tbl_val
        return from_doc_dflts(run, f"rPrDefault.{path}", optional)

    def _display_run_toggled(self, path: str) -> bool:
        run = cast("Run", self._proxy)
        direct_val = self._prop_run(path, True)
        if not isinstance(direct_val, NotFound):
            return on_off(direct_val)
        char_val = self._prop_run(path, True, "style")
        para_val = run.paragraph._prop(path, True, "paragraph-style")
        tbl_val = run.paragraph._prop(path, True, "table-style")
        found_count = sum(
            1
            for i in [char_val, para_val, tbl_val]
            if not isinstance(i, NotFound)
        )
        if found_count > 1:
            doc_val = on_off(
                from_doc_dflts(self._proxy, f"rPrDefault.{path}", True)
            )
            if doc_val is True:
                return doc_val
            return on_off(tbl_val) ^ on_off(para_val) ^ on_off(char_val)
        if not isinstance(char_val, NotFound):
            return on_off(char_val)
        if not isinstance(para_val, NotFound):
            return on_off(para_val)
        if not isinstance(tbl_val, NotFound):
            return on_off(tbl_val)
        return False

    def _prop_run_direct(self, path: str, optional: bool = False) -> Any:
        return self._proxy.prop(path, optional)

    def _prop_run_style(self, path: str, optional: bool = False) -> Any:
        run = cast("Run", self._proxy)
        if run.character_style:
            return from_style_inheritance(
                run, run.character_style, path, optional
            )
        return NotFound(self, path)

    def _prop_run(
        self,
        path: str,
        optional: bool = False,
        where: Literal["direct", "style", "both"] = "direct",
    ) -> Any:
        if where == "direct":
            return self._prop_run_direct(path, optional)
        elif where == "style":
            return self._prop_run_style(path, optional)
        direct_val = self._prop_run_direct(path, optional)
        if isinstance(direct_val, NotFound):
            return self._prop_run_style(path, optional)
        return direct_val
