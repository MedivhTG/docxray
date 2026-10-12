"""Provides the PackURI value type.

Also some useful known pack URI strings such as PACKAGE_URI.
"""

from __future__ import annotations

from pathlib import PurePosixPath
from posixpath import abspath, join, relpath
from typing import Self


class PackURI(str):
    def __new__(cls, path: str) -> Self:
        """Value type representing an OPC pack URI (a part name).

        Behaves as `str` otherwise. Always begins with a slash.
        """
        if not path.startswith("/"):
            raise ValueError(f"URI must with begin with slash: `{path}`")
        return str.__new__(cls, path)

    @property
    def baseURI(self) -> str:
        """Directory portion of this pack URI.

        Example: ``'/word'`` for ``'/word/document.xml'``.
        For the package pseudo-partname ``'/'``, returns ``'/'``.
        """
        return PurePosixPath(self).parent.as_posix()

    @property
    def ext(self) -> str:
        """File extension of this pack URI, without the leading dot.

        Example: ``'xml'`` for ``'/word/document.xml'``.
        Returns ``''`` if there is no extension.
        """
        return PurePosixPath(self).suffix.removeprefix(".")

    @property
    def filename(self) -> str:
        """Last segment of this pack URI.

        Example: ``'document.xml'`` for ``'/word/document.xml'``.
        Returns ``''`` for the package pseudo-partname ``'/'``.
        """
        return PurePosixPath(self).name

    @property
    def membername(self) -> str:
        """Pack URI with the leading slash stripped, the form used as a Zip member name.

        Example: ``'word/document.xml'`` for ``'/word/document.xml'``.
        Returns ``''`` for the package pseudo-partname ``'/'``.
        """
        return PurePosixPath(self).as_posix().removeprefix("/")

    @property
    def rels_uri(self) -> PackURI:
        """Pack URI of the ``.rels`` part associated with this part.

        Example: ``'/word/_rels/document.xml.rels'``
        for ``'/word/document.xml'``.
        """
        rels_filename = f"{self.filename}.rels"
        rels_uri_str = join(self.baseURI, "_rels", rels_filename)
        return PackURI(rels_uri_str)

    def relative_ref(self, baseURI: str) -> str:
        """Relative reference from `baseURI` to this pack URI.

        Example: for ``PackURI('/ppt/slideLayouts/slideLayout1.xml')``
        and ``baseURI='/ppt/slides'``, returns
        ``'../slideLayouts/slideLayout1.xml'``.
        """
        if baseURI == "/":
            return self.membername
        return relpath(self, baseURI)

    @staticmethod
    def from_rel_ref(baseURI: str, relative_ref: str) -> PackURI:
        """Absolute PackURI formed by resolving `relative_ref` against `baseURI`.

        Applies a workaround for packages whose paths do not follow OPC
        conventions, then normalize.

        Example: ``PackURI.from_rel_ref('/word/document.xml', '../media/image1.jpg')``
        returns ``PackURI('/word/media/image1.jpg')``.
        """
        rel_path = PurePosixPath(relative_ref)
        # Workaround for paths not followed OPC convetions (e.g.: r7-office/2024.4.2.721)
        # FIXME: probably will be removed with default paths as in Word app
        for part in rel_path.parts:
            baseURI = baseURI.removesuffix(part)
        # Remove dots, slashes, etc.
        return PackURI(abspath(join(baseURI, rel_path)))


PACKAGE_URI = PackURI("/")
CONTENT_TYPES_URI = PackURI("/[Content_Types].xml")
