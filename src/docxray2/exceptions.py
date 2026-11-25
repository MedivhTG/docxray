"""Module for base errors."""


class OxmlBaseError(Exception):
    pass


class OxmlAttrRequiredError(OxmlBaseError):
    pass


class OxmlAttrOptionalError(OxmlBaseError):
    pass


class OxmlExactlyOneError(OxmlBaseError):
    pass


class OxmlSequenceError(OxmlBaseError):
    pass


class OxmlChoiceOneError(OxmlBaseError):
    pass


class OxmlChoiceManyAtLeastOneError(OxmlBaseError):
    pass


class OxmlContentError(OxmlBaseError):
    pass


class DocxBaseError(Exception):
    pass


class DocxMissingPart(DocxBaseError):
    pass
