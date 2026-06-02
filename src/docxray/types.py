"""Standard types provided for project"""

from pathlib import Path
from typing import BinaryIO

type PkgFile = str | Path | BinaryIO
