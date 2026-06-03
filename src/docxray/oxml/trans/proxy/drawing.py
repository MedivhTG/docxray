# from functools import cached_property

from functools import cached_property
from typing import cast

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing, CT_PositiveSize2D
from docxray.oxml.trans.parts.image import ImagePart

# from docxray.oxml.trans.image.image import Image
from docxray.oxml.trans.proxy.image.picture import Picture
from docxray.oxml.trans.proxy.shared import ElementProxy, Emu, Length


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
    def width(self) -> Length:
        return self.size[0]

    @cached_property
    def height(self) -> Length:
        return self.size[1]

    @cached_property
    def size(self) -> tuple[Length, Length]:
        """Size of picture in WORD measured in Emu`s.

        Returns:
            tuple[Length, Length]: Width and height.
        """
        extent_elms: list[CT_PositiveSize2D] = self.element.xpath(
            "./wp:inline/wp:extent | ./wp:anchor/wp:extent"
        )
        extent_elm = extent_elms[0]
        return Emu(extent_elm.cx), Emu(extent_elm.cy)

    @cached_property
    def size_px(self) -> tuple[int, int]:
        width, height = self.size
        return width.px(), height.px()
