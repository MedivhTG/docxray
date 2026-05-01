"""|NumberingPart| and closely related objects."""

# docxray stuff
from docxray.opc.part import XmlPart
from docxray.oxml.numbering import CT_Numbering


class NumberingPart(XmlPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    pass
