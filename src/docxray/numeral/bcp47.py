import csv
from pathlib import Path

_DIR_ = Path(__file__).parent
_DFLT_SCRIPT_PATH_ = _DIR_ / "iso639-default-script.tsv"
_ICIDS_PATH_ = _DIR_ / "iso639-lcids.tsv"

with open(_DFLT_SCRIPT_PATH_, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    _ISO639_DEFAULT_SCRIPT_ = {}
    for row in reader:
        _ISO639_DEFAULT_SCRIPT_[row["tag3"]] = row["script"]

with open(_ICIDS_PATH_, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    _ISO639_ICIDS_ = {}
    for row in reader:
        _ISO639_ICIDS_[(row["tag1"], row["region"])] = (
            row["tag3"],
            row["script"],
        )


def script(locale: str) -> str:
    key = tuple(locale.split("-"))
    inf = _ISO639_ICIDS_.get(key)  # type: ignore[arg-type]
    if inf is None:
        raise ValueError(f"No such script for lang `{locale}`")
    tag3, script = inf
    if script:
        return script
    script = _ISO639_DEFAULT_SCRIPT_.get(tag3)
    if script is None:
        raise ValueError(f"No such script for lang `{locale}`")
    return script
