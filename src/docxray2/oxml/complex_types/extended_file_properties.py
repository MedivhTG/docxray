# docxray stuff
from docxray2.oxml.parser import Oxml


class OxmlNSExtendedFileProperties(Oxml, ns="ep"):
    pass


class CT_Properties(OxmlNSExtendedFileProperties):
    pass
