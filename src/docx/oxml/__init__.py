from docx.oxml.parser import register_element_cls

from .document import CT_Document

register_element_cls("w:document", CT_Document)
