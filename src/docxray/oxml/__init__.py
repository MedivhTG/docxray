# ruff: noqa: E402

# docxray stuff
from docxray.oxml.parser import register_element_cls

from .document import CT_Body, CT_Document

register_element_cls("w:document", CT_Document)
register_element_cls("w:body", CT_Body)

from .text.hyperlink import CT_Hyperlink
from .text.paragraph import CT_P
from .text.run import CT_R, CT_T

register_element_cls("w:p", CT_P)
register_element_cls("w:r", CT_R)
register_element_cls("w:t", CT_T)
register_element_cls("w:hyperlink", CT_Hyperlink)

from .table import CT_Tbl, CT_Tc

register_element_cls("w:tbl", CT_Tbl)
register_element_cls("w:tc", CT_Tc)

from .styles import CT_Style, CT_Styles

register_element_cls("w:styles", CT_Styles)
register_element_cls("w:style", CT_Style)

from .numbering import CT_Numbering

register_element_cls("w:numbering", CT_Numbering)
