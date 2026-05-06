from typing import Any, Self


class XsdBaseError(Exception):
    pass


class XsdTypeError(XsdBaseError):
    @classmethod
    def construct(cls, obj: Any, valid_type: type, extra: str = "") -> Self:
        msg = f"Invalid XSD type for `{obj}`, expected `{valid_type.__name__}`"
        if extra:
            msg += f": {extra}"
        return cls(msg)
