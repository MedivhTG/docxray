import metafile_render.gdi.objects as obj
import metafile_render.gdi.text as txt

from .wmf import _decode_ansi_text_with_symbols, _emit_text_with_symbols

txt._emit_text = _emit_text_with_symbols
txt._decode_ansi_text = _decode_ansi_text_with_symbols  # type: ignore[attr-defined]
obj._decode_ansi_text = _decode_ansi_text_with_symbols
