from enum import Enum
from typing import Any, TypeVar

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE
from docxray.enum.table import WD_CNF_FORMAT
from docxray.exceptions import InvalidXmlError

ENUM_T = TypeVar("ENUM_T", bound=Enum)


class SimpleTypes:
    @classmethod
    def validate_str(cls, obj: Any) -> str:
        if not isinstance(obj, str):
            msg = f"XML object {obj} is not a string"
            raise InvalidXmlError(msg)
        return obj

    @classmethod
    def validate_enum(cls, obj: Any, enum_cls: type[ENUM_T]) -> ENUM_T:
        if obj not in enum_cls.__members__.values():
            msg = f"XML object {obj} is not a member of enum {enum_cls}"
            raise InvalidXmlError(msg)
        return enum_cls(obj)


class ST_String(SimpleTypes):
    @classmethod
    def validate(cls, val: Any) -> str:
        return cls.validate_str(val)


class ST_OnOff(SimpleTypes):
    OFF_VALUES = {"0", "false", "off"}
    ON_VALUES = {"1", "true", "on"}

    @classmethod
    def validate(cls, val: Any) -> bool:
        if val in cls.OFF_VALUES:
            return False
        if val in cls.ON_VALUES:
            return True
        msg = f"Invalid OnOff value for {val}; MUST be in {cls.OFF_VALUES} or {cls.ON_VALUES}"
        raise InvalidXmlError(msg)


class ST_Cnf(SimpleTypes):
    BITS = "01"

    @classmethod
    def validate(cls, val: Any) -> WD_CNF_FORMAT:
        val_str = cls.validate_str(val)
        msg_pre = f"Invalid Cnf value for {val_str}; "
        if len(val_str) != 12:
            msg = f"{msg_pre}MUST be 12 chars length"
            raise InvalidXmlError(msg)
        if not set(val_str).issubset(cls.BITS):
            msg = f"{msg_pre}MUST be only bits {cls.BITS}"
            raise InvalidXmlError(msg)
        bit_mask = int(val_str[::-1], 2)
        return WD_CNF_FORMAT(bit_mask)


class ST_StyleType(SimpleTypes):
    @classmethod
    def validate(cls, type: Any) -> WD_STYLE_TYPE:
        return cls.validate_enum(type, WD_STYLE_TYPE)
