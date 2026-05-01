"""|NumberingPart| and closely related objects."""

# docxray stuff
from docxray.oxml.text.numbering import CT_Numbering

from ..opc.part import XmlPart


class NumberingPart(XmlPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    pass
