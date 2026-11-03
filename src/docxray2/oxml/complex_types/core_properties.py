# docxray stuff
from docxray2.oxml.parser import Oxml


class OxmlNSCoreProperties(Oxml, ns="cp"):
    pass


class CT_CoreProperties(OxmlNSCoreProperties):
    pass
