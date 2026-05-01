# ruff: noqa: E402

# docxray stuff
from docxray.oxml.parser import register_element_cls

from .document import CT_Body, CT_Document

register_element_cls("w:document", CT_Document)
register_element_cls("w:body", CT_Body)

from .text.hyperlink import CT_Hyperlink
from .text.paragraph import CT_P

register_element_cls("w:p", CT_P)
register_element_cls("w:hyperlink", CT_Hyperlink)

from .text.run import CT_R, CT_T

register_element_cls("w:r", CT_R)
register_element_cls("w:t", CT_T)

from .text.run_props import CT_I, CT_RPr, CT_RStyle

register_element_cls("w:rPr", CT_RPr)
register_element_cls("w:i", CT_I)
register_element_cls("w:rStyle", CT_RStyle)

from .table import CT_Tbl, CT_Tc, CT_Tr

register_element_cls("w:tbl", CT_Tbl)
register_element_cls("w:tr", CT_Tr)
register_element_cls("w:tc", CT_Tc)

from .styles import (
    CT_BasedOn,
    CT_DocDefaults,
    CT_RPrDefault,
    CT_Style,
    CT_Styles,
)

register_element_cls("w:rPrDefault", CT_RPrDefault)
register_element_cls("w:docDefaults", CT_DocDefaults)
register_element_cls("w:styles", CT_Styles)
register_element_cls("w:style", CT_Style)
register_element_cls("w:basedOn", CT_BasedOn)

from .numbering import CT_Numbering

register_element_cls("w:numbering", CT_Numbering)
