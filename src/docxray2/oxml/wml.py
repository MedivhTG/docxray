# docxray stuff
from docxray2.ns import NAMESPACE
from docxray2.xmlchemy import Nsmap

from .parser import Oxml

NSMAP: Nsmap = {"w": NAMESPACE.MAIN_DOCUMENT}


class OxmlNSWml(Oxml, ns="w", nsmap=NSMAP):
    pass


class CT_DocumentBase(OxmlNSWml):
    pass


class CT_Document(CT_DocumentBase):
    pass


# -------------------- ELEMENTS --------------------
class E_Document(CT_Document, tag="document"):
    pass
