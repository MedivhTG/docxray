# from functools import cached_property

from functools import cached_property
from typing import cast

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing

# from docxray.oxml.trans.image.image import Image
from docxray.oxml.trans.image.picture import Picture
from docxray.oxml.trans.parts.image import ImagePart
from docxray.oxml.trans.proxy.shared import ElementProxy


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
