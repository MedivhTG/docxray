import colorsys

# docxray stuff
from docxray.oxml.trans.st.enums import SE_THEME_COLOR

# TODO: get values from theme.xml
THEME_PALETTE = {
    SE_THEME_COLOR.DARK1: "#000000",
    SE_THEME_COLOR.LIGHT1: "#FFFFFF",
    SE_THEME_COLOR.DARK2: "#1E1E1E",
    SE_THEME_COLOR.LIGHT2: "#E7E7E7",
    SE_THEME_COLOR.ACCENT1: "#4472C4",
    SE_THEME_COLOR.ACCENT2: "#ED7D31",
    SE_THEME_COLOR.ACCENT3: "#A5A5A5",
    SE_THEME_COLOR.ACCENT4: "#FFC000",
    SE_THEME_COLOR.ACCENT5: "#5B9BD5",
    SE_THEME_COLOR.ACCENT6: "#70AD47",
    SE_THEME_COLOR.HYPERLINK: "#0563C1",
    SE_THEME_COLOR.FOLLOWED_HYPERLINK: "#954F72",
    SE_THEME_COLOR.BACKGROUND1: "#FFFFFF",
    SE_THEME_COLOR.TEXT1: "#000000",
    SE_THEME_COLOR.BACKGROUND2: "#E7E7E7",
    SE_THEME_COLOR.TEXT2: "#44546A",
}


class Colorize:
    @classmethod
    def theme_color(
        cls, theme: SE_THEME_COLOR, default: str = "#000000"
    ) -> str:
        return THEME_PALETTE.get(theme, default)

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
