"""|NumberingPart| and closely related objects."""

from functools import cached_property

# docxray stuff
from docxray.oxml.transitional.numbering import CT_Numbering
from docxray.oxml.transitional.part import TransitionalPart
from docxray.oxml.transitional.proxy.numbering.numbering import Numbering


class NumberingPart(TransitionalPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @cached_property
    def numbering(self) -> Numbering:
        return Numbering(self.element, self)
