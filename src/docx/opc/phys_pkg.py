"""Provides a general interface to a `physical` OPC package, such as a zip file."""

from __future__ import annotations

from abc import ABC, abstractmethod
import os
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from docx.opc.exceptions import PackageNotFoundError
from docx.opc.packuri import CONTENT_TYPES_URI, PackURI
from docx.types import PkgFile


def phys_pkg_reader(pkg_file: PkgFile) -> PhysPkgReader:
    """Factory function for physical package reader objects."""
    if isinstance(pkg_file, str | Path):
        if os.path.isdir(pkg_file):
            return _DirPkgReader(pkg_file)
        elif is_zipfile(pkg_file):
            return _ZipPkgReader(pkg_file)
        else:
            raise PackageNotFoundError("Package not found at '%s'" % pkg_file)
    else:  # assume it's a stream and pass it to Zip reader to sort out
        return _ZipPkgReader(pkg_file)


class PhysPkgReader(ABC):
    """Abstract base class for physical package readers."""

    @abstractmethod
    def blob_for(self, pack_uri: PackURI) -> bytes:
        """_summary_

        Args:
            pack_uri (PackURI): _description_

        Returns:
            bytes: _description_
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the package reader, releasing any resources."""
        ...

    @property
    @abstractmethod
    def content_types_xml(self) -> bytes:
        """Return the `[Content_Types].xml` blob from the package."""
        ...

    @abstractmethod
    def rels_xml_for(self, source_uri: PackURI) -> bytes | None:
        """Return rels item XML for source with `source_uri`, or None if no rels item."""
        ...


class _DirPkgReader(PhysPkgReader):
    """Implements |PhysPkgReader| interface for an OPC package extracted into a
    directory."""

    def __init__(self, path: str | Path):
        """`path` is the path to a directory containing an expanded package."""
        self._path = os.path.abspath(path)

    def blob_for(self, pack_uri: PackURI):
        """Return contents of file corresponding to `pack_uri` in package directory."""
        path = os.path.join(self._path, pack_uri.membername)
        with open(path, "rb") as f:
            blob = f.read()
        return blob

    def close(self):
        """Provides interface consistency with |ZipFileSystem|, but does nothing, a
        directory file system doesn't need closing."""
        pass

    @property
    def content_types_xml(self):
        """Return the `[Content_Types].xml` blob from the package."""
        return self.blob_for(CONTENT_TYPES_URI)

    def rels_xml_for(self, source_uri: PackURI):
        """Return rels item XML for source with `source_uri`, or None if the item has no
        rels item."""
        try:
            rels_xml = self.blob_for(source_uri.rels_uri)
        except IOError:
            rels_xml = None
        return rels_xml


class _ZipPkgReader(PhysPkgReader):
    """Implements |PhysPkgReader| interface for a zip file OPC package."""

    def __init__(self, pkg_file: PkgFile) -> None:
        self._zipf = ZipFile(pkg_file, "r")

    def blob_for(self, pack_uri: PackURI) -> bytes:
        """Return blob corresponding to `pack_uri`.

        Raises |ValueError| if no matching member is present in zip archive.
        """
        return self._zipf.read(pack_uri.membername)

    def close(self) -> None:
        """Close the zip archive, releasing any resources it is using."""
        self._zipf.close()

    @property
    def content_types_xml(self) -> bytes:
        """Return the `[Content_Types].xml` blob from the zip package."""
        return self.blob_for(CONTENT_TYPES_URI)

    def rels_xml_for(self, source_uri: PackURI) -> bytes | None:
        """Return rels item XML for source with `source_uri` or None if no rels item is
        present."""
        try:
            rels_xml = self.blob_for(source_uri.rels_uri)
        except KeyError:
            rels_xml = None
        return rels_xml
