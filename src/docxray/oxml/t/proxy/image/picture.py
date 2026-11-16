from __future__ import annotations

from functools import cached_property
from io import BytesIO

from metafile_render import render_metafile
from PIL import Image

from .wmf import wmf_type


class UnrecognizedPictureError(Exception):
    pass


class Picture:
    def __init__(self, blob: bytes) -> None:
        self._blob = blob
        self.__load_image__(blob)

    def __load_image__(self, blob: bytes) -> None:
        if wmf_type(blob):
            self._img = Image.open(BytesIO(self._wmf_to_png(blob)))
        else:
            self._img = Image.open(BytesIO(blob))

    @cached_property
    def content_type(self) -> str:
        ct = self._img.get_format_mimetype()
        if ct is None:
            raise UnrecognizedPictureError(
                "Mime type of image was `None` (created in code?)"
            )
        return ct

    @cached_property
    def width(self) -> int:
        return self.size[0]

    @cached_property
    def height(self) -> int:
        return self.size[1]

    @cached_property
    def size(self) -> tuple[int, int]:
        return self._img.size

    @cached_property
    def blob(self) -> bytes:
        return self._blob

    def resized(self, size: tuple[int, int]) -> Picture:
        with self._img.copy() as cloned:
            cloned = cloned.resize(size, Image.Resampling.LANCZOS)
            out = BytesIO()
            cloned.save(out, format=self._img.format or "PNG")
            out.seek(0)
            return Picture(out.read())

    def _wmf_to_png(self, blob: bytes) -> bytes:
        wmf_result = render_metafile(blob)
        return wmf_result.data
