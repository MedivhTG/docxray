"""Module for base errors."""


class OxmlBaseError(Exception):
    pass


class OxmlAttrRequiredError(OxmlBaseError):
    pass


class OxmlAttrOptionalError(OxmlBaseError):
    pass


class OxmlContentError(OxmlBaseError):
    pass


class DocxBaseError(Exception):
    pass


class DocxMissingPart(DocxBaseError):
    pass
