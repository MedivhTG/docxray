# docxray stuff
from docxray.exceptions import InvalidXmlError


class ST_OnOff:
    OFF_VALUES = {"0", "false", "off"}
    ON_VALUES = {"1", "true", "on"}

    @classmethod
    def validate(cls, val: str) -> bool:
        if val in cls.OFF_VALUES:
            return False
        if val in cls.ON_VALUES:
            return True
        msg = f"Invalid OnOff value for {val}"
        raise InvalidXmlError(msg)
