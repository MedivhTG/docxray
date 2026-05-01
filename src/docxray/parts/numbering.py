"""|NumberingPart| and closely related objects."""

from functools import cached_property

# docxray stuff
from docxray.numbering.numbering import Numbering
from docxray.opc.part import XmlPart
from docxray.oxml.numbering import CT_Numbering


class NumberingPart(XmlPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @cached_property
    def numbering(self) -> Numbering:
        return Numbering(self.element, self)
