from pathlib import PurePosixPath
from typing import Self

SLASH = "/"


class PkgURI(str):
    def __new__(cls, uri: str) -> Self:
        if not uri.startswith(SLASH):
            raise ValueError(f"URI must with begin with slash: `{uri}`")
        return str.__new__(cls, uri)

    def __init__(self, uri: str) -> None:
        super().__init__()
        self._path = PurePosixPath(uri)

    @property
    def member_name(self) -> str:
        return self._path.as_posix().removeprefix(SLASH)


CONTENT_TYPES_PKG_URI = PkgURI("/[Content_Types].xml")
