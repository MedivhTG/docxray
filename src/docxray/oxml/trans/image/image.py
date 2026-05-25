from __future__ import annotations

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


class UnrecognizedImageError(Exception):
    pass


class Image:
    def __init__(self, blob: bytes) -> None:
        self.__img_lib: ImgLib = IMG_LIB
        self.__img_lib_version = IMG_LIB_VERSION
        self.__img_interface = self.__load_img_interface(blob)

    def __load_img_interface(self, blob: bytes) -> WandImage | ImageFile:
        from wand.image import Image as WandImage

        wmf_t = wmf_type(blob)

        if self.__img_lib == "wand":
            if wmf_t:
                blob = self.__wmf_to_png(blob)

            return WandImage(blob=blob)
        else:
            if wmf_t:
                msg = f"Type `{wmf_t}` cannot be parsed by {self.__img_lib}.{self.__img_lib_version}"
                raise UnrecognizedImageError(msg)
            return PillowImage.open(blob)

    def __wmf_to_png(self, wmf_blob: bytes) -> bytes:
        msg = f"Lib {self.__img_lib}.{self.__img_lib_version} cannot parse img"
        if self.__img_lib == "wand":
            from wand.image import Image as WandImage

            with WandImage(blob=wmf_blob) as img:
                png_blob = img.make_blob(format="png")
                if png_blob is None:
                    raise UnrecognizedImageError(msg)
                return cast("bytes", png_blob)
        raise UnrecognizedImageError(msg)
