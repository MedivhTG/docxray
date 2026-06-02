from __future__ import annotations

from functools import cached_property
from io import BytesIO
from typing import TYPE_CHECKING, Literal, cast

from PIL import Image as PillowImage
from PIL.ImageFile import ImageFile

from .wmf import wmf_type

type ImgLib = Literal["wand", "pillow"]
IMG_LIB: ImgLib

if TYPE_CHECKING:
    from wand.image import Image as WandImage


try:
    # Importing api automatically starts checking
    # installed ImageMagick application
    from wand import api  # noqa
    from wand import VERSION

    IMG_LIB = "wand"
    IMG_LIB_VERSION = VERSION
except ImportError:
    # Fallback if ImageMagick is not installed
    from PIL import __version__

    IMG_LIB = "pillow"
    IMG_LIB_VERSION = __version__


class UnrecognizedPictureError(Exception):
    pass


class Picture:
    def __init__(self, blob: bytes) -> None:
        self.__blob = blob
        self.__img_lib: ImgLib = IMG_LIB
        self.__img_lib_version = IMG_LIB_VERSION
        self.__img_interface = self.__load_img_interface(blob)

    @cached_property
    def content_type(self) -> str:
        err = UnrecognizedPictureError(
            "Mime type of image was `None` (created in code?)"
        )
        if isinstance(self.__img_interface, ImageFile):
            ct = self.__img_interface.get_format_mimetype()
            if ct is None:
                raise err
            return ct
        ct = self.__img_interface.mimetype
        if ct is None:
            raise err
        return ct

    @cached_property
    def width(self) -> int:
        return self.size[0]

    @cached_property
    def height(self) -> int:
        return self.size[1]

    @cached_property
    def size(self) -> tuple[int, int]:
        if isinstance(self.__img_interface, ImageFile):
            return self.__img_interface.size
        return self.__img_interface.size

    @cached_property
    def blob(self) -> bytes:
        return self.__blob

    def resized(self, size: tuple[int, int]) -> Picture:
        """Get resized copy of an Picture with passed size.

        Args:
            size (tuple[int, int]): Width and height in pixels.
        """
        if self.__img_lib == "wand":
            return self._resized_wand(size)
        return self._resized_pillow(size)

    def _resized_wand(self, size: tuple[int, int]) -> Picture:
        from wand.image import Image as WandImage

        img = self.__img_interface
        if not isinstance(img, WandImage):
            raise TypeError("Expected WandImage instance")

        with img.clone() as cloned:
            cloned.resize(*size)
            blob = cloned.make_blob()
            if blob is None:
                raise ValueError("Bytes was `None` while resizing with wand")
            return Picture(blob)

    def _resized_pillow(self, size: tuple[int, int]) -> Picture:
        img = self.__img_interface
        if not isinstance(img, ImageFile):
            raise TypeError("Expected ImageFile instance")
        with img.copy() as cloned:
            cloned.thumbnail(size, PillowImage.Resampling.LANCZOS)
            out = BytesIO()
            cloned.save(out, format=img.format or "PNG")
            out.seek(0)
            return Picture(out.read())

    def __load_img_interface(self, blob: bytes) -> WandImage | ImageFile:
        from wand.image import Image as WandImage

        wmf_t = wmf_type(blob)

        if self.__img_lib == "wand":
            if wmf_t:
                blob = self.__wmf_to_png(blob)
                self.__blob = blob
            return WandImage(blob=blob)
        else:
            if wmf_t:
                msg = f"Type `{wmf_t}` cannot be parsed by {self.__img_lib}.{self.__img_lib_version}"
                raise UnrecognizedPictureError(msg)
            return PillowImage.open(blob)

    def __wmf_to_png(self, wmf_blob: bytes) -> bytes:
        msg = f"Lib {self.__img_lib}.{self.__img_lib_version} cannot parse img"
        if self.__img_lib == "wand":
            from wand.image import Image as WandImage

            with WandImage(blob=wmf_blob) as img:
                png_blob = img.make_blob(format="png")
                if png_blob is None:
                    raise UnrecognizedPictureError(msg)
                return cast("bytes", png_blob)
        raise UnrecognizedPictureError(msg)
