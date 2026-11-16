from enum import StrEnum
from functools import lru_cache
from math import atan2, cos, degrees, radians, sin
from pathlib import Path

from fontTools.agl import toUnicode
from fontTools.ttLib import TTFont
from metafile_render.commands import DrawTextCommand, TextAlignment
from metafile_render.font import measure_text_advance
from metafile_render.gdi.constants import (
    _ETO_CLIPPED,
    _ETO_GLYPH_INDEX,
    _ETO_OPAQUE,
    _TA_UPDATECP,
)
from metafile_render.gdi.objects import _charset_codec
from metafile_render.gdi.playback import _Playback
from metafile_render.geometry import rectangle_path, vector_length
from metafile_render.primitives import ClipOperation, Point, Rect
from metafile_render.text_layout import TextLayoutError


class WmfMimeType(StrEnum):
    WMF = "image/wmf"
    EMF = "image/emf"


# BigEndian to LittleEndian
WMF_PH_KEY = bytes.fromhex("D7 CD C6 9A")
WMF_RAW_TYPE_1 = bytes.fromhex("01 00")
WMF_RAW_TYPE_2 = bytes.fromhex("02 00")
WMF_RAW_HEADER_SIZE = bytes.fromhex("09 00")
WMF_RAW_VERSION_1 = bytes.fromhex("00 01")
WMF_RAW_VERSION_3 = bytes.fromhex("00 03")

EMR_HEADER_TYPE = bytes.fromhex("01 00 00 00")
EMR_ENHMETA_SIGNATURE = bytes.fromhex("20 45 4D 46")


def wmf_type(wmf_blob: bytes) -> WmfMimeType | None:
    """Determine mime type of hypothetical WMF blob.

    Analyzes the image with signature bytes or structure
    (shallow view) of WMF/EMF files.

    Args:
        wmf_blob (bytes): Image blob.
    """
    if is_wmf(wmf_blob):
        return WmfMimeType.WMF
    if is_emf(wmf_blob):
        return WmfMimeType.EMF
    return None


def is_wmf(blob: bytes) -> bool:
    if len(blob) < 18:
        return False

    return blob.startswith(WMF_PH_KEY) or (
        blob[:2] in (WMF_RAW_TYPE_1, WMF_RAW_TYPE_2)
        and blob[2:4] == WMF_RAW_HEADER_SIZE
        and blob[4:6] in (WMF_RAW_VERSION_1, WMF_RAW_VERSION_3)
    )


def is_emf(blob: bytes) -> bool:
    return (
        len(blob) >= 88
        and blob[:4] == EMR_HEADER_TYPE
        and blob[40:44] == EMR_ENHMETA_SIGNATURE
    )


_SYMBOL_CMAP = TTFont(Path(__file__).parent / "fonts" / "Symbol.ttf")[
    "cmap"
].getcmap(3, 0)
_SYMBOL_CMAP_MAP: dict[int, str] = _SYMBOL_CMAP.cmap if _SYMBOL_CMAP else {}


@lru_cache
def symbol_char(code: int) -> str | None:
    if code in _SYMBOL_CMAP_MAP:
        return toUnicode(_SYMBOL_CMAP_MAP[code])
    return None


def _decode_symbol_text(raw: bytes) -> str:
    result: list[str] = []
    for b in raw:
        char = symbol_char(b)
        if char is None:
            char = symbol_char(0xF000 + b)
        result.append(char if char is not None else chr(b))
    return "".join(result)


def _decode_ansi_text_with_symbols(raw: bytes, charset: int) -> str:
    if charset == 1:  # SYMBOL_CHARSET
        return _decode_symbol_text(raw)
    return raw.decode(_charset_codec(charset), errors="replace")


# TODO: look for braces and other
def _emit_text_with_symbols(
    playback: _Playback,
    *,
    text: str,
    reference: Point,
    options: int,
    bounds: Rect | None,
    advances: list[Point] | None,
) -> None:

    if not text:
        return
    if options & _ETO_GLYPH_INDEX:
        playback.warn(
            "glyph_index_text",
            "glyph-index text was replaced with visible placeholder glyphs",
        )
        text = "□" * len(text)
    original_text = text
    text, retained_indices = playback.context.clean_text(text)
    update_current = bool(playback.state.text_align & _TA_UPDATECP)
    logical_origin = (
        playback.state.current_position if update_current else reference
    )
    origin = playback.map_point(logical_origin)
    positions: list[Point] = []
    advance_end: Point | None = None
    original_font = font = playback.state.font
    # There is some cases with constructed left/right braces as one char on Symbols..
    # Than it's too hard for rendering and we must deeply change logic of this sidelib
    if font.charset == 1:
        playback.state.font = font = type(font)(
            face_name="STIX Two Math",
            height=font.height,
            width=font.width,
            escapement=font.escapement,
            orientation=font.orientation,
            weight=font.weight,
            italic=font.italic,
            underline=font.underline,
            strikeout=font.strikeout,
            charset=0,
        )
    try:
        if advances:
            cursor_x, cursor_y = logical_origin
            for index, _character in enumerate(original_text):
                positions.append(playback.map_point((cursor_x, cursor_y)))
                if index < len(advances):
                    cursor_x += advances[index][0]
                    cursor_y += advances[index][1]
            advance_end = playback.map_point((cursor_x, cursor_y))
            if update_current:
                playback.state.current_position = (cursor_x, cursor_y)
            if retained_indices is not None:
                positions = [positions[index] for index in retained_indices]
        elif update_current:
            try:
                advance = measure_text_advance(font, text)
            except TextLayoutError:
                playback.context.warn_text(
                    "text_layout_failed",
                    "skipped text whose advance could not be laid out",
                )
                text = ""
            else:
                angle = radians(font.escapement / 10.0)
                playback.state.current_position = (
                    logical_origin[0] + advance * cos(angle),
                    logical_origin[1] - advance * sin(angle),
                )
        if not text and not (bounds is not None and options & _ETO_OPAQUE):
            return
        mapped_height = vector_length(
            playback.map_vector((0.0, font.height or -12.0))
        )
        baseline_vector = playback.map_vector((1.0, 0.0))
        rotation = (
            degrees(atan2(baseline_vector[1], baseline_vector[0]))
            + font.escapement / 10.0
        )
        mapped_bounds: Rect | None = None
        if bounds is not None and (options & (_ETO_OPAQUE | _ETO_CLIPPED)):
            corners = [
                playback.map_point((bounds.left, bounds.top)),
                playback.map_point((bounds.right, bounds.top)),
                playback.map_point((bounds.right, bounds.bottom)),
                playback.map_point((bounds.left, bounds.bottom)),
            ]
            mapped_bounds = Rect(
                min(point[0] for point in corners),
                min(point[1] for point in corners),
                max(point[0] for point in corners),
                max(point[1] for point in corners),
            )
        clip = playback.state.clip
        if mapped_bounds is not None and options & _ETO_CLIPPED:
            clip = playback.clip_with_operation(
                ClipOperation(rectangle_path(mapped_bounds), "and")
            )
        playback.append_command(
            DrawTextCommand(
                text=text,
                origin=origin,
                positions=tuple(positions),
                font=font,
                font_height=max(mapped_height, 1.0),
                rotation=rotation,
                color=playback.state.text_color,
                background_color=playback.state.background_color,
                opaque=bool(options & _ETO_OPAQUE)
                or playback.state.background_mode == 2,
                bounds=mapped_bounds,
                clip=clip,
                advance_end=advance_end,
                alignment=TextAlignment.from_gdi(playback.state.text_align),
            )
        )
    finally:
        playback.state.font = original_font
