"""Module with exceptions used for XSD validation"""

from typing import Any, Self


class XsdBaseError(Exception):
    """Standard error for XSD validation."""


class XsdTypeError(XsdBaseError):
    @classmethod
    def construct(cls, obj: Any, valid_type: type, extra: str = "") -> Self:
        """Cosntruct standard XSD error for raise.

        Args:
            obj (Any): Given object for repesentation.
            valid_type (type): XSD type validation cls.
            extra (str, optional): Extra info for error. Defaults to "".

        Returns:
            Self: Constructed `XsdTypeError`
        """
        msg = f"Invalid XSD type for object `{obj}` of type `{obj.__class__.__name__}`, expected `{valid_type.__name__}`"
        if extra:
            msg += f": {extra}"
        return cls(msg)
