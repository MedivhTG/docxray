# ruff: noqa: E402

# docxray stuff
from docxray.oxml.parser import register_element_cls

from .document import CT_Body, CT_Document
from .shared import CT_OnOff, CT_String

register_element_cls("w:document", CT_Document)
register_element_cls("w:body", CT_Body)


from .text.paragraph import CT_P

register_element_cls("w:p", CT_P)

from .text.paragraph_props import CT_PPr

register_element_cls("w:pPr", CT_PPr)
register_element_cls("w:pStyle", CT_String)

from .text.hyperlink import CT_Hyperlink

register_element_cls("w:hyperlink", CT_Hyperlink)

from .text.run import CT_R, CT_T

register_element_cls("w:r", CT_R)
register_element_cls("w:t", CT_T)

from .text.run_props import CT_RPr

register_element_cls("w:rPr", CT_RPr)
register_element_cls("w:i", CT_OnOff)
register_element_cls("w:rStyle", CT_String)

from .table import CT_Row, CT_Tbl, CT_Tc

register_element_cls("w:tbl", CT_Tbl)
register_element_cls("w:tr", CT_Row)
register_element_cls("w:tc", CT_Tc)

from .table_props import CT_Cnf, CT_TblPr, CT_TcPr, CT_TrPr

register_element_cls("w:tblPr", CT_TblPr)
register_element_cls("w:trPr", CT_TrPr)
register_element_cls("w:tcPr", CT_TcPr)
register_element_cls("w:cnfStyle", CT_Cnf)
register_element_cls("w:tblStyle", CT_String)

from .styles import (
    CT_DocDefaults,
    CT_RPrDefault,
    CT_Style,
    CT_Styles,
)

register_element_cls("w:docDefaults", CT_DocDefaults)
register_element_cls("w:rPrDefault", CT_RPrDefault)
register_element_cls("w:styles", CT_Styles)
register_element_cls("w:style", CT_Style)
register_element_cls("w:basedOn", CT_String)

from .numbering import CT_Numbering

register_element_cls("w:numbering", CT_Numbering)
