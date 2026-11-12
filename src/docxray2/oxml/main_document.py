# docxray stuff
from docxray2.oxml.parser import Oxml


class OxmlNSWml(Oxml, ns="w"):
    pass


class CT_DocumentBase(OxmlNSWml):
    pass


class CT_Document(CT_DocumentBase):
    pass


# -------------------- ELEMENTS --------------------
class E_Document(CT_Document, tag="document"):
    pass
