from functools import lru_cache
from locale import LC_ALL, getlocale, setlocale


# TODO: if locale will be UTF-8 or other.. need refac
@lru_cache
def os_locale() -> str:
    """Get system current locale in format like `en-US`."""
    setlocale(LC_ALL, "")
    locale_tuple = getlocale()
    return f"{locale_tuple[0] or ""}-{locale_tuple[1] or ""}"
