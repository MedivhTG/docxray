"""|NumberingPart| and closely related objects."""

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.numbering import CT_Numbering
from docxray.oxml.trans.part import TransitionalPart
from docxray.oxml.trans.proxy.numbering.numbering import Numbering


class NumberingPart(TransitionalPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @cached_property
    def numbering(self) -> Numbering:
        return Numbering(self.element, self)
