"""XSD module errors"""


class XsdBaseError(Exception):
    pass


class XsdValidationError(XsdBaseError):
    pass


class XsdStringifyError(XsdBaseError):
    pass
