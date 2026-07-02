from importlib.metadata import version

from .api import Document

__version__ = version("docxray")
VERSION = __version__


__all__ = ["Document"]
