"""Module for base OXML errors."""


class OxmlBaseError(Exception):
    pass


class OxmlAttrRequiredError(OxmlBaseError):
    pass


class OxmlAttrOptionalError(OxmlBaseError):
    pass


class OxmlContentError(OxmlBaseError):
    pass
