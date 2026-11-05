from __future__ import annotations

import posixpath
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
    def baseURI(self) -> str:
        return self._path.parent.as_posix()

    @property
    def file_name(self) -> str:
        return self._path.name

    @property
    def ext(self) -> str:
        return self._path.suffix.removeprefix(".")

    @property
    def member_name(self) -> str:
        return self._path.as_posix().removeprefix(SLASH)

    @property
    def rels_uri(self) -> PkgURI:
        rels_filename = f"{self.file_name}.rels"
        rels_uri_str = posixpath.join(self.baseURI, "_rels", rels_filename)
        return PkgURI(rels_uri_str)

    def relative_ref(self, baseURI: str) -> str:
        return self[1:] if baseURI == "/" else posixpath.relpath(self, baseURI)

    @staticmethod
    def from_rel_ref(baseURI: str, relative_ref: str) -> PkgURI:
        rel_path = PurePosixPath(relative_ref)
        return PkgURI(posixpath.abspath(posixpath.join(baseURI, rel_path)))


PKG_URI = PkgURI("/")
CONTENT_TYPES_PKG_URI = PkgURI("/[Content_Types].xml")
