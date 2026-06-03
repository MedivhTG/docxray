"""|NumberingPart| and closely related objects."""

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.numbering import CT_Numbering
from docxray.oxml.trans.part import TransitionalPart
from docxray.oxml.trans.proxy.numbering.numbering import Numbering
from docxray.oxml.trans.proxy.styles.styles import Styles


class NumberingPart(TransitionalPart[CT_Numbering]):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @cached_property
    def numbering(self) -> Numbering:
        """`Numbering` instance with list properties."""
        return Numbering(self.element, self)

    @cached_property
    def styles(self) -> Styles:
        """|DocumentPart| object for this package."""
        package = self.package
        assert package is not None
        return package.main_document_part.styles
