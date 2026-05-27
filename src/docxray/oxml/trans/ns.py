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


class XML:
    SPACE = qn("xml:space")


class W:
    BACKGROUND = qn("w:background")

    BODY = qn("w:body")
    ALT_CHUNK = qn("w:altChunk")

    R = qn("w:r")

    TR = qn("w:tr")
    TC = qn("w:tc")

    SECT_PR = qn("w:sectPr")
    FRAME_PR = qn("w:framePr")

    TEXT_DIRECTION = qn("w:textDirection")

    P_PR = qn("w:pPr")
    KEEP_NEXT = qn("w:keepNext")
    KEEP_LINES = qn("w:keepLines")
    PAGE_BREAK_BEFORE = qn("w:pageBreakBefore")
    WIDOW_CONTROL = qn("w:widowControl")
    SUPPRESS_LINE_NUMBERS = qn("w:suppressLineNumbers")
    P_BDR = qn("w:pBdr")
    TABS = qn("w:tabs")
    SUPPRESS_AUTO_HYPHENS = qn("w:suppressAutoHyphens")
    KINSOKU = qn("w:kinsoku")
    WORD_WRAP = qn("w:wordWrap")
    OVERFLOW_PUNCT = qn("w:overflowPunct")
    TOP_LINE_PUNCT = qn("w:topLinePunct")
    AUTO_SPACE_DE = qn("w:autoSpaceDE")
    AUTO_SPACE_DN = qn("w:autoSpaceDN")
    BIDI = qn("w:bidi")
    ADJUST_RIGHT_IND = qn("w:adjustRightInd")

    IND = qn("w:ind")
    START_CHARS = qn("w:startChars")
    END = qn("w:end")
    END_CHARS = qn("w:endChars")
    LEFT_CHARS = qn("w:leftChars")
    RIGHT_CHARS = qn("w:rightChars")
    HANGING = qn("w:hanging")
    HANGING_CHARS = qn("w:hangingChars")
    FIRST_LINE = qn("w:firstLine")
    FIRST_LINE_CHARS = qn("w:firstLineChars")

    CONTEXTUAL_SPACING = qn("w:contextualSpacing")
    MIRROR_INDENTS = qn("w:mirrorIndents")
    SUPPRESS_OVERLAP = qn("w:suppressOverlap")
    JC = qn("w:jc")
    TEXT_ALIGNMENT = qn("w:textAlignment")
    TEXTBOX_TIGHT_WRAP = qn("w:textboxTightWrap")
    OUTLINE_LVL = qn("w:outlineLvl")
    DIV_ID = qn("w:divId")

    NUM_PR = qn("w:numPr")
    ILVL = qn("w:ilvl")
    NUM_ID = qn("w:numId")
    NUMBERING_CHANGE = qn("w:numberingChange")
    INS = qn("w:ins")

    R_PR = qn("w:rPr")

    R_FONTS = qn("w:rFonts")
    HINT = qn("w:hint")
    ASCII = qn("w:ascii")
    H_ANSI = qn("w:hAnsi")
    ASCII_THEME = qn("w:asciiTheme")
    H_ANSI_THEME = qn("w:hAnsiTheme")
    EAST_ASIA_THEME = qn("w:eastAsiaTheme")
    CSTHEME = qn("w:cstheme")

    B = qn("w:b")
    B_CS = qn("w:bCs")
    I_CS = qn("w:iCs")
    CAPS = qn("w:caps")
    SMALL_CAPS = qn("w:smallCaps")
    STRIKE = qn("w:strike")
    DSTRIKE = qn("w:dstrike")
    OUTLINE = qn("w:outline")
    SHADOW = qn("w:shadow")
    EMBOSS = qn("w:emboss")
    IMPRINT = qn("w:imprint")
    NO_PROOF = qn("w:noProof")
    SNAP_TO_GRID = qn("w:snapToGrid")
    VANISH = qn("w:vanish")
    WEB_HIDDEN = qn("w:webHidden")
    SPACING = qn("w:spacing")
    W = qn("w:w")
    KERN = qn("w:kern")
    POSITION = qn("w:position")
    SZ = qn("w:sz")
    SZ_CS = qn("w:szCs")
    HIGHLIGHT = qn("w:highlight")
    U = qn("w:u")
    EFFECT = qn("w:effect")
    BDR = qn("w:bdr")
    FIT_TEXT = qn("w:fitText")
    VERT_ALIGN = qn("w:vertAlign")
    RTL = qn("w:rtl")
    CS = qn("w:cs")
    EM = qn("w:em")
    LANG = qn("w:lang")
    EAST_ASIAN_LAYOUT = qn("w:eastAsianLayout")
    SPEC_VANISH = qn("w:specVanish")
    O_MATH = qn("w:oMath")

    TBL_PR = qn("w:tblPr")
    TBL_STYLE_ROW_BAND_SIZE = qn("w:tblStyleRowBandSize")
    TBL_STYLE_COL_BAND_SIZE = qn("w:tblStyleColBandSize")
    TBL_PR_EX = qn("w:tblPrEx")
    TBL_LOOK = qn("w:tblLook")
    FIRST_ROW = qn("w:firstRow")
    LAST_ROW = qn("w:lastRow")
    FIRST_COLUMN = qn("w:firstColumn")
    LAST_COLUMN = qn("w:lastColumn")
    NO_H_BAND = qn("w:noHBand")
    NO_V_BAND = qn("w:noVBande")
    TBL_CELL_SPACING = qn("w:tblCellSpacing")
    TR_PR = qn("w:trPr")

    TC_PR = qn("w:tcPr")
    TC_W = qn("w:tcW")
    GRID_SPAN = qn("w:gridSpan")
    H_MERGE = qn("w:hMerge")
    V_MERGE = qn("w:vMerge")

    TBL_BORDERS = qn("w:tblBorders")
    TC_BORDERS = qn("w:tcBorders")
    TOP = qn("w:top")
    LEFT = qn("w:left")
    BOTTOM = qn("w:bottom")
    RIGHT = qn("w:right")
    INSIDE_H = qn("w:insideH")
    INSIDE_V = qn("w:insideV")
    TL_2_BR = qn("w:tl2br")
    TR_2_BL = qn("w:tr2bl")

    THEME_COLOR = qn("w:themeColor")
    THEME_TINT = qn("w:themeTint")
    THEME_SHADE = qn("w:themeShade")
    SPACE = qn("w:space")
    FRAME = qn("w:frame")

    SHD = qn("w:shd")
    NO_WRAP = qn("w:noWrap")
    TC_MAR = qn("w:tcMar")
    TC_FIT_TEXT = qn("w:tcFitText")
    V_ALIGN = qn("w:vAlign")
    HIDE_MARK = qn("w:hideMark")
    COLOR = qn("w:color")

    R_STYLE = qn("w:rStyle")
    P_STYLE = qn("w:pStyle")
    TBL_STYLE = qn("w:tblStyle")
    CNF_STYLE = qn("w:cnfStyle")

    TBL_STYLE_PR = qn("w:tblStylePr")

    I = qn("w:i")  # noqa: E741
    T = qn("w:t")

    DOC_DEFAULTS = qn("w:docDefaults")
    R_PR_DEFAULT = qn("w:rPrDefault")

    LATENT_STYLES = qn("w:latentStyles")

    STYLE = qn("w:style")
    STYLE_ID = qn("w:styleId")
    BASED_ON = qn("w:basedOn")
    DEFAULT = qn("w:default")
    CUSTOM_STYLE = qn("w:customStyle")
    NAME = qn("w:name")
    ALIASES = qn("w:aliases")
    NEXT = qn("w:next")
    LINK = qn("w:link")
    AUTO_REDEFINE = qn("w:autoRedefine")
    HIDDEN = qn("w:hidden")
    UI_PRIORITY = qn("w:uiPriority")
    SEMI_HIDDEN = qn("w:semiHidden")
    UNHIDE_WHEN_USED = qn("w:unhideWhenUsed")
    Q_FORMAT = qn("w:qFormat")
    LOCKED = qn("w:locked")
    PERSONAL = qn("w:personal")
    PERSONAL_COMPOSE = qn("w:personalCompose")
    PERSONAL_REPLY = qn("w:personalReply")

    NUM_PIC_BULLET = qn("w:numPicBullet")

    ABSTRACT_NUM = qn("w:abstractNum")
    NUM = qn("w:num")
    NUM_ID_MAC_AT_CLEANUP = qn("w:numIdMacAtCleanup")
    ABSTRACT_NUM_ID = qn("w:abstractNumId")
    LVL_OVERRIDE = qn("w:lvlOverride")
    START_OVERRIDE = qn("w:startOverride")
    MULTI_LEVEL_TYPE = qn("w:multiLevelType")
    TMPL = qn("w:tmpl")
    STYLE_LINK = qn("w:styleLink")
    NUM_STYLE_LINK = qn("w:numStyleLink")

    LVL = qn("w:lvl")
    TPLC = qn("w:tplc")
    TENTATIVE = qn("w:tentative")
    START = qn("w:start")

    NUM_FMT = qn("w:numFmt")
    FORMAT = qn("w:format")

    LVL_RESTART = qn("w:lvlRestart")
    IS_LGL = qn("w:isLgl")
    SUFF = qn("w:suff")
    LVL_TEXT = qn("w:lvlText")
    LVL_PIC_BULLET_ID = qn("w:lvlPicBulletId")
    LEGACY = qn("w:legacy")
    LVL_JC = qn("w:lvlJc")

    R_PR_CHANGE = qn("w:rPrChange")
    AUTHOR = qn("w:author")
    DATE = qn("w:date")
    RSID = qn("w:rsid")
    NSID = qn("w:nsid")
    RSID_R_PR = qn("w:rsidRPr")
    RSID_R = qn("w:rsidR")
    RSID_DEL = qn("w:rsidDel")
    RSID_P = qn("w:rsidP")
    RSID_R_DEFAULT = qn("w:rsidRDefault")

    THEME_FONT_LANG = qn("w:themeFontLang")
    EAST_ASIA = qn("w:eastAsia")

    TAB = qn("w:tab")

    TYPE = qn("w:type")
    CLEAR = qn("w:clear")
    FONT = qn("w:font")
    CHAR = qn("w:char")
    VAL = qn("w:val")
    NULL = qn("w:null")
    ID = qn("w:id")
    ORIGINAL = qn("w:original")


class WP:
    ANCHOR = qn("wp:anchor")
    INLINE = qn("wp:inline")

    EXTENT = qn("wp:extent")
    EFFECT_EXTENT = qn("wp:effectExtent")
    DOC_PR = qn("wp:docPr")
    C_NV_GRAPHIC_FRAM_PR = qn("wp:cNvGraphicFramePr")


class A:
    GRAPHIC = qn("a:graphic")
    GRAPHIC_DATA = qn("a:graphicData")

    BLIP = qn("a:blip")


class PIC:
    PIC = qn("pic:pic")

    NV_PIC_PR = qn("pic:nvPicPr")
    C_NV_PR = qn("pic:cNvPr")
    C_NV_PIC_PR = qn("pic:cNvPicPr")

    BLIP_FILL = qn("pic:blipFill")
    SP_PR = qn("pic:spPr")


class R:
    EMBED = qn("r:embed")


class NoNS:
    CX = "cx"
    CY = "cy"

    DIST_T = "distT"
    DIST_B = "distB"
    DIST_L = "distL"
    DIST_R = "distR"

    URI = "uri"
