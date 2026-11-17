from __future__ import annotations

from base64 import b64encode
from io import BytesIO
from logging import warning

from metafile_render import MetafileError, render_metafile
from PIL import Image
from PIL.ImageFile import ImageFile

from .wmf import wmf_type

VECTOR_IMAGE_RENDER_DPI = 200
PLACEHOLDER_SIZE = (50, 50)
PLACEHOLDER_COLOR = (240, 240, 240)


class UnrecognizedPictureError(Exception):
    pass


class Picture:
    def __init__(
        self,
        blob: bytes,
        size_hint: tuple[int, int] | None = None,
        eager_load: bool = False,
    ) -> None:
        self._blob = blob
        self._wmf_type = wmf_type(blob)
        self._size_hint = size_hint
        self._svg_data: bytes | None = None
        self._pil_img: ImageFile | None = None
        if eager_load:
            self.__load_image__(blob)

    def __load_image__(self, blob: bytes) -> None:
        if self._wmf_type:
            img_inf = self._wmf_to_svg_or_png(blob)
            if img_inf is None:
                img_buf = self._png_placeholder()
                self._pil_img = Image.open(img_buf)
            else:
                img_data, is_svg = img_inf
                if is_svg:
                    self._svg_data = img_data
                else:
                    self._pil_img = Image.open(BytesIO(img_data))
        else:
            self._pil_img = Image.open(BytesIO(blob))

    def load(self, size_hint: tuple[int, int] | None = None) -> None:
        self._size_hint = size_hint
        self.__load_image__(self._blob)

    def render_img_src_base64(
        self, rastr_size: tuple[int, int] | None = None
    ) -> str:
        size = rastr_size or self._size_hint
        if self.is_wmf:
            payload = self._svg_data
            if payload is None:
                placeholder = self._png_placeholder(size)
                return f"data:image/png;base64,{b64encode(placeholder.getvalue()).decode()}"
            return f"data:image/svg+xml;base64,{b64encode(payload).decode()}"
        if size:
            pic = self.resized(size)
            return f"data:{self.content_type};base64,{b64encode(pic._blob).decode()}"
        return (
            f"data:{self.content_type};base64,{b64encode(self._blob).decode()}"
        )

    @property
    def is_wmf(self) -> bool:
        return bool(self._wmf_type)

    @property
    def content_type(self) -> str:
        if not self._pil_img:
            if not self._svg_data:
                raise ValueError("Image not loaded")
            return "image/svg+xml"
        ct = self._pil_img.get_format_mimetype()
        if ct is None:
            raise UnrecognizedPictureError(
                "Mime type of image was `None` (created in code?)"
            )
        return ct

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def size(self) -> tuple[int, int]:
        if self._pil_img is None:
            if self._size_hint is None:
                raise ValueError("Size not intialized")
            return self._size_hint
        return self._pil_img.size

    @property
    def blob(self) -> bytes:
        return self._blob

    @property
    def img(self) -> ImageFile:
        if not self._pil_img:
            raise ValueError("Image not loaded OR it's vector image")
        return self._pil_img

    def resized(
        self, size: tuple[int, int], eager_load: bool = False
    ) -> Picture:
        if self._svg_data:
            return self
        with self.img.copy() as cloned:
            cloned = cloned.resize(size, Image.Resampling.LANCZOS)
            out = BytesIO()
            cloned.save(out, format=self.img.format or "PNG")
            out.seek(0)
            return Picture(out.read(), size, eager_load)

    def _png_placeholder(
        self, render_size: tuple[int, int] | None = None
    ) -> BytesIO:
        size = render_size or self._size_hint or PLACEHOLDER_SIZE
        img = Image.new("RGB", size, PLACEHOLDER_COLOR)
        buf = BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        return buf

    def _wmf_to_svg_or_png(self, blob: bytes) -> tuple[bytes, bool] | None:
        size_hint = self._size_hint
        is_svg = False
        try:
            rendered = render_metafile(
                blob,
                output_format="svg",
                dpi=VECTOR_IMAGE_RENDER_DPI,
                size_hint=size_hint,
                backend="auto",
            )
            is_svg = True
        except MetafileError as e:
            warning(
                f"Generated SVG cannot be consumed safely: {e}. Falling back to PNG."
            )
            try:
                rendered = render_metafile(
                    blob,
                    output_format="png",
                    dpi=VECTOR_IMAGE_RENDER_DPI,
                    size_hint=size_hint,
                    backend="auto",
                )
            except MetafileError as png_e:
                warning(
                    f"Failed to render PNG fallback with metafile-render: {png_e}. Using placeholder instead."
                )
                return None
        return rendered.data, is_svg
