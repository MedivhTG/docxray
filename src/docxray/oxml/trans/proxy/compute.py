# docxray stuff
from docxray.constants import PCT_TO_PERCENT_RATIO
from docxray.oxml.trans.shared import CT_OnOff, CT_TblWidth
from docxray.oxml.trans.st.enums import SE_OnOff1, SE_TblWidth

from .shared import Twips


def normalize_pct(pct: int) -> float:
    return pct / PCT_TO_PERCENT_RATIO


def width(width_elm: CT_TblWidth) -> Twips | float | None:
    if (
        width_elm.type in (SE_TblWidth.NULL, SE_TblWidth.AUTO, None)
        or width_elm.w is None
    ):
        return None
    # TODO: here we can catch bug with old patterns as mm, cm etc.
    # Hope no old docs will be loaded
    width_int = int(width_elm.w)
    if width_elm.type == SE_TblWidth.TWIPS:
        return Twips(width_int)
    return normalize_pct(width_int)


def on_off(on_off: CT_OnOff | bool | None) -> bool:
    if isinstance(on_off, bool):
        return on_off
    if on_off is None:
        return True
    if isinstance(on_off.val, bool):
        return on_off.val
    if on_off.val is None:
        return True
    if on_off.val == SE_OnOff1.ON:
        return True
    return False
