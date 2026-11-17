from __future__ import annotations

from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.t.proxy.drawing import Drawing

from .base import HtmlBuilder

if TYPE_CHECKING:
    # docxray stuff
    from docxray.transform.ruleset import RuleSet


class HtmlDrawing(HtmlBuilder["Drawing"]):
    @classmethod
    def element(cls, proxy: Drawing, ruleset: RuleSet) -> HtmlElement:
        return Element("img", cls._attrs(proxy))

    @classmethod
    def _attrs(cls, proxy: Drawing) -> dict[str, str]:
        pic = proxy.picture
        if pic is None:
            return {
                "width": f"{proxy.width.px()}px",
                "height": f"{proxy.height.px()}px",
                "alt": proxy.name,
            }
        return {
            "src": pic.render_img_src_base64(),
            # When it's rendered as vector we must sure that image will not
            # cross other tags in browser
            "width": f"{proxy.width.px()}px",
            "height": f"{proxy.height.px()}px",
            "alt": proxy.name,
        }
