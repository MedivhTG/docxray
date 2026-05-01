"""Enumerations related to styles."""

from enum import StrEnum


class WD_STYLE_TYPE(StrEnum):
    """Specifies one of the four style types: paragraph, character, list, or table.

    Example::

        from docx import Document
        from docx.enum.style import WD_STYLE_TYPE

        styles = Document().styles
        assert styles[0].type == WD_STYLE_TYPE.PARAGRAPH

    MS API name: `WdStyleType`

    http://msdn.microsoft.com/en-us/library/office/ff196870.aspx
    """

    CHARACTER = "character"
    LIST = "numbering"
    PARAGRAPH = "paragraph"
    TABLE = "table"
