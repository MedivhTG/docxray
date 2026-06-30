from __future__ import annotations

from base64 import b64encode
from typing import TYPE_CHECKING

from lxml.html import Element, HtmlElement

# docxray stuff
from docxray.oxml.trans.proxy.drawing import Drawing

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
        base64 = b64encode(pic.resized(proxy.size_px).blob).decode()
        return {
            "src": f"data:{pic.content_type};base64,{base64}",
            "alt": proxy.name,
        }
