from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.opc.part import Part
from docxray.oxml.trans.proxy.image.picture import Picture


class ImagePart(Part):
    @cached_property
    def picture(self) -> Picture:
        return Picture(self.blob)
