from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.opc.part import Part
from docxray.oxml.trans.image.image import Image


class ImagePart(Part):
    @cached_property
    def image(self) -> Image:
        return Image(self.blob)
