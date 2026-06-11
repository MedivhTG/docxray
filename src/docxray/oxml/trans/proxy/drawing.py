# from functools import cached_property

from functools import cached_property
from typing import Any, cast

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing, CT_PositiveSize2D
from docxray.oxml.trans.parts.image import ImagePart

# from docxray.oxml.trans.image.image import Image
from docxray.oxml.trans.proxy.image.picture import Picture
from docxray.oxml.trans.proxy.shared import (
    ElementProxy,
    Emu,
    Length,
    NotFound,
    PropertyPath,
    safe_get_prop,
)


# TODO: if need to get hard, then go for another properties like:
# 1) Effects
# 2) Wrapping
# 3) Rototate
# 4) Anchor processing
class Drawing(ElementProxy[CT_Drawing]):
    @cached_property
    def picture(self) -> Picture | None:
        """Bitmap image inside of WORD. Can be Anchor or Inline.

        If `None`, then:
        1) There is no bitmap image
        2) There is no reference to bitmap image
        3) There is outside link of bitmap image
        """
        pic_rIds = self.element.xpath(
            ".//pic:pic/pic:blipFill/a:blip/@r:embed"
        )
        if not pic_rIds:
            return None
        return cast("ImagePart", self.part.related_parts[pic_rIds[0]]).picture

    @cached_property
    def identifier(self) -> int:
        """Unique identifier for Word."""
        return self._doc_pr_prop("id")

    @cached_property
    def name(self) -> str:
        """Hidden name of an drawing object."""
        return self._doc_pr_prop("name")

    @cached_property
    def description(self) -> str:
        """Hidden description of an drawing object."""
        return self._doc_pr_prop("descr")

    @cached_property
    def width(self) -> Length:
        """Drawing width render in Word (not the width of the image file!)"""
        return self.size[0]

    @cached_property
    def height(self) -> Length:
        """Drawing height render in Word (not the height of the image file!)"""
        return self.size[1]

    @cached_property
    def size(self) -> tuple[Length, Length]:
        """Size (width, height) of picture in WORD measured in Emu`s."""
        extent_elm: CT_PositiveSize2D = self._get_inside_prop(
            PropertyPath.base("extent")
        )
        return Emu(extent_elm.cx), Emu(extent_elm.cy)

    @cached_property
    def size_px(self) -> tuple[int, int]:
        """Size (width, height) of picture in WORD measured in pixels (default dpi)."""
        width, height = self.size
        return width.px(), height.px()

    def _doc_pr_prop(self, name: str) -> Any:
        return self._get_inside_prop(PropertyPath.base(name, "docPr"))

    def _get_inside_prop(
        self, path: PropertyPath, optional: bool = False
    ) -> Any:
        drawing: Any = self.element.inline
        if drawing is None:
            drawing = self.element.anchor
        if drawing is None:
            return NotFound(drawing, path)
        return safe_get_prop(drawing, path, optional)
