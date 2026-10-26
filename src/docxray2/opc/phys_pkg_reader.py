from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from zipfile import ZipFile, is_zipfile

# docxray stuff
from docxray2.opc.exceptions import OpcPackageNotFoundError

from ..types import PkgFile
from .pkg_uri import CONTENT_TYPES_PKG_URI, PkgURI


def phys_pkg_reader(pkg_file: PkgFile) -> PhysPkgReader:
    if isinstance(pkg_file, str | Path):
        if os.path.isdir(pkg_file):
            return _DirPkgReader(pkg_file)
        elif is_zipfile(pkg_file):
            return _ZipPkgReader(pkg_file)
        else:
            raise OpcPackageNotFoundError(f"Package not found at '{pkg_file}'")
    else:
        return _ZipPkgReader(pkg_file)


class PhysPkgReader(ABC):
    @abstractmethod
    def close(self) -> None: ...

    @property
    @abstractmethod
    def content_types_xml(self) -> bytes: ...

    @abstractmethod
    def blob_for(self, pkg_uri: PkgURI) -> bytes: ...


class _ZipPkgReader(PhysPkgReader):
    def __init__(self, pkg_file: PkgFile) -> None:
        self._zipf = ZipFile(pkg_file)
        self._namel = set(self._zipf.namelist())

    @property
    def content_types_xml(self) -> bytes:
        return self.blob_for(CONTENT_TYPES_PKG_URI)

    def blob_for(self, pkg_uri: PkgURI) -> bytes:
        return self._zipf.read(pkg_uri.member_name)

    def close(self) -> None:
        self._zipf.close()


class _DirPkgReader(PhysPkgReader):
    def __init__(self, path: str | Path) -> None:
        self._path = os.path.abspath(path)

    @property
    def content_types_xml(self) -> bytes:
        return self.blob_for(CONTENT_TYPES_PKG_URI)

    def blob_for(self, pkg_uri: PkgURI) -> bytes:
        path = os.path.join(self._path, pkg_uri.member_name)
        with open(path, "rb") as f:
            blob = f.read()
        return blob

    def close(self) -> None:
        pass
