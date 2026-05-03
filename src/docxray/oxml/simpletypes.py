from abc import abstractmethod
from enum import Enum
from typing import Any, TypeVar

# docxray stuff
from docxray.enum.style import WD_STYLE_TYPE, WD_TBL_STYLE_OVERRIDE_TYPE
from docxray.enum.table import WD_CNF_FORMAT
from docxray.exceptions import InvalidXmlError

ENUM_T = TypeVar("ENUM_T", bound=Enum)


class SimpleType:
    @classmethod
    @abstractmethod
    def validate(cls, obj: Any) -> Any: ...

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


class ST_String(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> str:
        return cls.validate_str(obj)


class ST_OnOff(SimpleType):
    OFF_VALUES = {"0", "false", "off"}
    ON_VALUES = {"1", "true", "on"}

    @classmethod
    def validate(cls, obj: Any) -> bool:
        if obj in cls.OFF_VALUES:
            return False
        if obj in cls.ON_VALUES:
            return True
        msg = f"Invalid OnOff value for {obj}; MUST be in {cls.OFF_VALUES} or {cls.ON_VALUES}"
        raise InvalidXmlError(msg)


class ST_Cnf(SimpleType):
    BITS = "01"

    @classmethod
    def validate(cls, obj: Any) -> WD_CNF_FORMAT:
        val_str = cls.validate_str(obj)
        msg_pre = f"Invalid Cnf value for {val_str}; "
        if len(val_str) != 12:
            msg = f"{msg_pre}MUST be 12 chars length"
            raise InvalidXmlError(msg)
        if not set(val_str).issubset(cls.BITS):
            msg = f"{msg_pre}MUST be only bits {cls.BITS}"
            raise InvalidXmlError(msg)
        bit_mask = int(val_str[::-1], 2)
        return WD_CNF_FORMAT(bit_mask)


class ST_StyleType(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> WD_STYLE_TYPE:
        return cls.validate_enum(obj, WD_STYLE_TYPE)


class ST_TblStyleOverrideType(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> WD_TBL_STYLE_OVERRIDE_TYPE:
        return cls.validate_enum(obj, WD_TBL_STYLE_OVERRIDE_TYPE)
