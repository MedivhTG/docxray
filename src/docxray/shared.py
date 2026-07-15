"""Standard functionality provided for project"""

import ctypes
from functools import lru_cache


@lru_cache
def win32_color_hex(idx: int) -> str:
    """Get system color from Win32 by color index.

    Args:
        idx (int): Color index.

    Returns:
        str: Hex-color in format `#RRGGBB`.
    """

    color = ctypes.windll.user32.GetSysColor(idx)
    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"
