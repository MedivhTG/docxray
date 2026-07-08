from functools import cached_property
from typing import Literal

# docxray stuff
from docxray.oxml.t.proxy.base import ElementProxy
from docxray.oxml.t.settings import CT_Settings
from docxray.oxml.t.st.enums import SE_WML_COLOR_SCHEME_INDEX as C

type SemanticColor = Literal[
    "bg1",
    "t1",
    "bg2",
    "t2",
    "accent1",
    "accent2",
    "accent3",
    "accent4",
    "accent5",
    "accent6",
    "hyperlink",
    "followedHyperlink",
]
THEME_COLOR_MAPPING_DEFAULTS: dict[SemanticColor, C] = {
    "bg1": C.LIGHT1,
    "t1": C.DARK1,
    "bg2": C.LIGHT2,
    "t2": C.DARK2,
    "accent1": C.ACCENT1,
    "accent2": C.ACCENT2,
    "accent3": C.ACCENT3,
    "accent4": C.ACCENT4,
    "accent5": C.ACCENT5,
    "accent6": C.ACCENT6,
    "hyperlink": C.HYPERLINK,
    "followedHyperlink": C.FOLLOWED_HYPERLINK,
}


class Settings(ElementProxy[CT_Settings]):
    @cached_property
    def theme_color_mapping(self) -> dict[SemanticColor, C]:
        def _color(name: SemanticColor, idx: C | None) -> C:
            if idx is None:
                return THEME_COLOR_MAPPING_DEFAULTS[name]
            return idx

        clrSchemeMapping_elm = self.element.clrSchemeMapping
        if clrSchemeMapping_elm is None:
            return THEME_COLOR_MAPPING_DEFAULTS
        return {
            "bg1": _color("bg1", clrSchemeMapping_elm.bg1),
            "t1": _color("t1", clrSchemeMapping_elm.t1),
            "bg2": _color("bg2", clrSchemeMapping_elm.bg2),
            "t2": _color("t2", clrSchemeMapping_elm.t2),
            "accent1": _color("accent1", clrSchemeMapping_elm.accent1),
            "accent2": _color("accent2", clrSchemeMapping_elm.accent2),
            "accent3": _color("accent3", clrSchemeMapping_elm.accent3),
            "accent4": _color("accent4", clrSchemeMapping_elm.accent4),
            "accent5": _color("accent5", clrSchemeMapping_elm.accent5),
            "accent6": _color("accent6", clrSchemeMapping_elm.accent6),
            "hyperlink": _color("hyperlink", clrSchemeMapping_elm.hyperlink),
            "followedHyperlink": _color(
                "followedHyperlink", clrSchemeMapping_elm.followedHyperlink
            ),
        }
