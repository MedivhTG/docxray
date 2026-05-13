import re
from typing import cast

# docxray stuff
from docxray.constants import PCT_TO_PERCENT_RATIO
from docxray.oxml.trans.shared import CT_OnOff, CT_TblWidth
from docxray.oxml.trans.st.enums import SE_OnOff1, SE_TblWidth
from docxray.oxml.trans.st.shared_common import ST_UniversalMeasure
from docxray.xsd.facets import PatternFacet

from .shared import Cm, Inches, Length, Mm, NotFound, Pica, Pt, Twips


def normalize_pct(pct: float) -> float:
    return pct / PCT_TO_PERCENT_RATIO


def width(
    width_elm: CT_TblWidth, ignore_pct: bool = False
) -> Length | float | None:
    """Compute width of anything that has width measure.

    If return `Length` instance, then it's numbered width,
    else if it's float, then it's percents, else auto.

    Args:
        width_elm (CT_TblWidth): Width element from XML.
        ignore_pct (bool, optional): Ignore percents if it's not
            needed. Defaults to False.

    Returns:
        Length | float | None: Length in number, percents or auto (`None`).
    """
    if (
        width_elm.type in (SE_TblWidth.NULL, SE_TblWidth.AUTO, None)
        or width_elm.w is None
    ):
        return None
    if isinstance(width_elm.w, str):
        return width_string(width_elm.w)
    width_float = float(width_elm.w)
    if width_elm.type == SE_TblWidth.TWIPS:
        return Twips(width_float)
    if ignore_pct:
        return None
    return normalize_pct(width_float)


def width_string(width: str) -> Length | None:
    pattern = cast("PatternFacet", ST_UniversalMeasure.FACETS["pattern"]).value
    if pattern is None:
        return None
    match = re.compile(pattern).fullmatch(width.strip())
    if not match:
        return None

    integer_part = match.group(1)
    decimal_part = match.group(2)
    unit = match.group(3)

    num_str = integer_part + (decimal_part if decimal_part else "")
    value = float(num_str)

    match unit:
        case "mm":
            return Mm(value)
        case "cm":
            return Cm(value)
        case "in":
            return Inches(value)
        case "pt":
            return Pt(value)
        case "pc" | "pi":
            return Pica(value)
        case _:
            return None


def on_off(on_off: NotFound | None | bool | SE_OnOff1 | CT_OnOff) -> bool:
    def _val(val: None | bool | SE_OnOff1) -> bool:
        if val is None:
            return True
        if isinstance(val, bool):
            return val
        if isinstance(val, SE_OnOff1):
            if val == SE_OnOff1.ON:
                return True
            return False

    if isinstance(on_off, NotFound):
        return False
    if isinstance(on_off, CT_OnOff):
        return _val(on_off.val)
    return _val(on_off)
