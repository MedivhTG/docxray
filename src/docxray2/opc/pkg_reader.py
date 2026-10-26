from ..types import PkgFile
from .phys_pkg_reader import phys_pkg_reader


class PkgReader:
    @staticmethod
    def from_file(pkg_file: PkgFile) -> "PkgReader":
        pkg_reader = phys_pkg_reader(pkg_file)
        pkg_reader.close()
        return PkgReader()
