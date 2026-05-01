# docxray stuff
from docxray.oxml.parser import register_element_cls

from .document import CT_Body, CT_Document
from .styles import CT_Style, CT_Styles
from .text.numbering import CT_Numbering

register_element_cls("w:document", CT_Document)
register_element_cls("w:body", CT_Body)

register_element_cls("w:style", CT_Style)
register_element_cls("w:styles", CT_Styles)

register_element_cls("w:numbering", CT_Numbering)
