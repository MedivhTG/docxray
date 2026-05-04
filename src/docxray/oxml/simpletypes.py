from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, TypeVar

# docxray stuff
from docxray.enum.word import (
    WD_CNF_FORMAT,
    WD_MERGE,
    WD_MULTILEVEL_TYPE,
    WD_STYLE_TYPE,
    WD_TBL_STYLE_OVERRIDE_TYPE,
    WD_UNDERLINE,
    WD_VERTICAL_ALIGN_RUN,
)
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


class ST_DateTime(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> datetime:
        val_str = cls.validate_str(obj)
        if val_str.endswith("Z"):
            val_str = val_str.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(val_str)
        except ValueError as e:
            msg = f"Invalid DateTime value for {obj}; MUST be datetime (iso); internal err {e}"
            raise InvalidXmlError(msg)


class ST_DecimalNumber(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> int:
        try:
            return int(obj)
        except (ValueError, TypeError):
            msg = f"Invalid DecimalNumber value for {obj}; MUST be integer"
            raise InvalidXmlError(msg)


class ST_LongHexNumber(SimpleType):
    OCTETS = 4
    HEX = 16

    @classmethod
    def validate(cls, obj: Any) -> int:
        val_str = cls.validate_str(obj)
        try:
            val_bytes = bytes.fromhex(val_str)
            if len(val_bytes) != cls.OCTETS:
                msg = f"Invalid LongHexNumber value for {obj}; MUST have only {cls.OCTETS} (bytes)"
                raise InvalidXmlError(msg)
            return int(val_str, cls.HEX)
        except ValueError:
            msg = (
                f"Invalid LongHexNumber value for {obj}; MUST be an hex string"
            )
            raise InvalidXmlError(msg)


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


class ST_Merge(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> WD_MERGE:
        return cls.validate_enum(obj, WD_MERGE)


class ST_VerticalAlignRun(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> WD_VERTICAL_ALIGN_RUN:
        return cls.validate_enum(obj, WD_VERTICAL_ALIGN_RUN)


class ST_Underline(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> WD_UNDERLINE:
        return cls.validate_enum(obj, WD_UNDERLINE)


class ST_MultiLevelType(SimpleType):
    @classmethod
    def validate(cls, obj: Any) -> WD_MULTILEVEL_TYPE:
        return cls.validate_enum(obj, WD_MULTILEVEL_TYPE)
