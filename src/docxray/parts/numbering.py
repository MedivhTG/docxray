"""|NumberingPart| and closely related objects."""

from functools import cached_property

# docxray stuff
from docxray.opc.part import XmlPart
from docxray.oxml.transitional.numbering import CT_Numbering
from docxray.proxy.numbering.numbering import Numbering


class NumberingPart(XmlPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @cached_property
    def numbering(self) -> Numbering:
        return Numbering(self.element, self)
