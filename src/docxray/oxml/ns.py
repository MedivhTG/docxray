"""Namespace-related objects."""

from __future__ import annotations

nsmap = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcmitype": "http://purl.org/dc/dcmitype/",
    "dcterms": "http://purl.org/dc/terms/",
    "dgm": "http://schemas.openxmlformats.org/drawingml/2006/diagram",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "sl": "http://schemas.openxmlformats.org/schemaLibrary/2006/main",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


def qn(tag: str) -> str:
    """Stands for "qualified name".

    This utility function converts a familiar namespace-prefixed tag name like "w:p"
    into a Clark-notation qualified tag name for lxml. For example, `qn("w:p")` returns
    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p".
    """
    prefix, tagroot = tag.split(":")
    uri = nsmap[prefix]
    return "{%s}%s" % (uri, tagroot)


class W:
    BACKGROUND = qn("w:background")

    BODY = qn("w:body")
    ALT_CHUNK = qn("w:altChunk")

    TR = qn("w:tr")
    TC = qn("w:tc")

    SECT_PR = qn("w:sectPr")
    P_PR = qn("w:pPr")
    R_PR = qn("w:rPr")
    TBL_PR = qn("w:tblPr")
    TR_PR = qn("w:trPr")
    TC_PR = qn("w:tcPr")

    TC_W = qn("w:tcW")
    GRID_SPAN = qn("w:gridSpan")
    H_MERGE = qn("w:hMerge")
    V_MERGE = qn("w:vMerge")
    TC_BORDERS = qn("w:tcBorders")
    SHD = qn("w:shd")
    NO_WRAP = qn("w:noWrap")
    TC_MAR = qn("w:tcMar")
    TEXT_DIRECTION = qn("w:textDirection")
    TC_FIT_TEXT = qn("w:tcFitText")
    V_ALIGN = qn("w:vAlign")
    HIDE_MARK = qn("w:hideMark")

    R_STYLE = qn("w:rStyle")
    P_STYLE = qn("w:pStyle")
    TBL_STYLE = qn("w:tblStyle")
    CNF_STYLE = qn("w:cnfStyle")

    TBL_STYLE_PR = qn("w:tblStylePr")

    I = qn("w:i")  # noqa: E741
    T = qn("w:t")

    DOC_DEFAULTS = qn("w:docDefaults")
    R_PR_DEFAULT = qn("w:rPrDefault")

    STYLE = qn("w:style")
    STYLE_ID = qn("w:styleId")
    BASED_ON = qn("w:basedOn")

    TYPE = qn("w:type")
    VAL = qn("w:val")
