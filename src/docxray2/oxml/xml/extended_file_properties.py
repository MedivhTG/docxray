# docxray stuff
from docxray2.oxml.parser import Oxml


class OxmlNSExtendedFileProperties(Oxml, ns="ep"):
    pass


class CT_Properties(OxmlNSExtendedFileProperties):
    pass


# -------------------- ELEMENTS --------------------


class E_Properties(CT_Properties, tag="Properties"):
    pass
