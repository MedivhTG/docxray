import colorsys

# docxray stuff
from docxray.oxml.t.proxy.theme import ThemeColor
from docxray.oxml.t.st.enums import SE_HEX_COLOR_AUTO, SE_THEME_COLOR


class Colorize:
    # TODO: do i need research?
    @classmethod
    def colorize(
        cls,
        color: SE_HEX_COLOR_AUTO | bytes,
        theme: SE_THEME_COLOR | None = None,
        theme_palette: dict[SE_THEME_COLOR, ThemeColor] | None = None,
        theme_tint: bytes | None = None,
        theme_shade: bytes | None = None,
        default: str = "#000000",
        prefer_theme: bool = False,
    ) -> str:
        """Get final color from given params.

        **NOTE**: Word acts weird here, so sometimes
        (in very rare cases) you can get color as defined in schema, but Word app uses
        other, e.g. `accent2` instead of `accent3` on `auto`.

        Args:
            color (SE_HEX_COLOR_AUTO | bytes): If it's an bytes instance -> hex-format color `RRGGBB`,
                else compute with theme or return default.
            theme (SE_THEME_COLOR | None, optional): Used theme for colorize. Defaults to None.
            theme_palette (dict[SE_THEME_COLOR, ThemeColor] | None, optional): Theme palette of and document.
                Defaults to None.
            theme_tint (bytes | None, optional): Theme tint for base theme color
                from 0 to 255 in hex-format. Defaults to None.
            theme_shade (bytes | None, optional): Theme shade for base theme color
                from 0 to 255 in hex-format. Defaults to None.
            default (str, optional): Used default hex-color if no others are found. Defaults to "#000000".
            prefer_theme (bool, optional): Prefer theme color compute over passed `color` param if can.
                Defaults to False.

        Returns:
            str: Hex-format color string, e.g. black as "#000000".
        """

        if prefer_theme:
            if theme:
                return cls._theme_colorize(
                    theme, theme_palette, theme_tint, theme_shade, default
                )
            elif isinstance(color, SE_HEX_COLOR_AUTO):
                return default
            return f"#{color.hex().upper()}"
        if isinstance(color, SE_HEX_COLOR_AUTO):
            return cls._theme_colorize(
                theme, theme_palette, theme_tint, theme_shade, default
            )
        return f"#{color.hex().upper()}"

    @classmethod
    def hex_to_rgb(cls, hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]

    @classmethod
    def rgb_to_hex(cls, rgb: tuple) -> str:
        return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

    @classmethod
    def rgb_to_hsl(cls, rgb: tuple) -> tuple[float, float, float]:
        r, g, b = [x / 255.0 for x in rgb]
        h, l_, s = colorsys.rgb_to_hls(r, g, b)
        return (h * 360, s, l_)

    @classmethod
    def hsl_to_rgb(cls, hsl: tuple) -> tuple[int, int, int]:
        h, s, l_ = hsl
        r, g, b = colorsys.hls_to_rgb(h / 360, l_, s)
        return tuple(int(x * 255) for x in (r, g, b))  # type: ignore[return-value]

    @classmethod
    def apply_tint(cls, base_color_hex: str, tint_hex: str) -> str:
        tint_percent = int(tint_hex, 16) / 255.0
        rgb_base = cls.hex_to_rgb(base_color_hex)
        h, s, l_ = cls.rgb_to_hsl(rgb_base)
        l_new = l_ * tint_percent + (1 - tint_percent)
        rgb_new = cls.hsl_to_rgb((h, s, l_new))
        return cls.rgb_to_hex(rgb_new)

    @classmethod
    def apply_shade(cls, base_color_hex: str, shade_hex: str) -> str:
        shade_percent = int(shade_hex, 16) / 255.0
        rgb_base = cls.hex_to_rgb(base_color_hex)
        h, s, l_ = cls.rgb_to_hsl(rgb_base)
        l_new = l_ * shade_percent
        rgb_new = cls.hsl_to_rgb((h, s, l_new))
        return cls.rgb_to_hex(rgb_new)

    @classmethod
    def _theme_colorize(
        cls,
        theme: SE_THEME_COLOR | None = None,
        theme_palette: dict[SE_THEME_COLOR, ThemeColor] | None = None,
        theme_tint: bytes | None = None,
        theme_shade: bytes | None = None,
        default: str = "#000000",
    ) -> str:
        if theme is None:
            return default
        if theme and theme_palette:
            base_color = theme_palette[theme].color or default
        else:
            base_color = default
        if theme_tint:
            return Colorize.apply_tint(base_color, theme_tint.hex())
        elif theme_shade:
            return Colorize.apply_shade(base_color, theme_shade.hex())
        return base_color
