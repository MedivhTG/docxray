# ruff: noqa: E402

# docxray stuff
from docxray.oxml.parser import register_element_cls

from .document import CT_Body, CT_Document
from .shared import (
    CT_Border,
    CT_Cnf,
    CT_Color,
    CT_DecimalNumber,
    CT_EastAsianLayout,
    CT_Em,
    CT_FitText,
    CT_Fonts,
    CT_FramePr,
    CT_Highlight,
    CT_HpsMeasure,
    CT_Jc,
    CT_Language,
    CT_LongHexNumber,
    CT_OnOff,
    CT_Shd,
    CT_SignedHpsMeasure,
    CT_String,
    CT_TextDirection,
    CT_TextEffect,
    CT_TextScale,
    CT_TrackChange,
)

register_element_cls("w:rsid", CT_LongHexNumber)
register_element_cls("w:name", CT_String)

register_element_cls("w:document", CT_Document)
register_element_cls("w:body", CT_Body)


from .text.paragraph import CT_P

register_element_cls("w:p", CT_P)

from .text.paragraph_props import (
    CT_Ind,
    CT_PBdr,
    CT_PPr,
    CT_Tabs,
    CT_TextAlignment,
    CT_TextboxTightWrap,
)

register_element_cls("w:pPr", CT_PPr)
register_element_cls("w:pStyle", CT_String)
register_element_cls("w:keepNext", CT_OnOff)
register_element_cls("w:keepLines", CT_OnOff)
register_element_cls("w:pageBreakBefore", CT_OnOff)
register_element_cls("w:framePr", CT_FramePr)
register_element_cls("w:widowControl", CT_OnOff)
register_element_cls("w:suppressLineNumbers", CT_OnOff)
register_element_cls("w:pBdr", CT_PBdr)
register_element_cls("w:shd", CT_Shd)
register_element_cls("w:tabs", CT_Tabs)
register_element_cls("w:suppressAutoHyphens", CT_OnOff)
register_element_cls("w:kinsoku", CT_OnOff)
register_element_cls("w:wordWrap", CT_OnOff)
register_element_cls("w:overflowPunct", CT_OnOff)
register_element_cls("w:topLinePunct", CT_OnOff)
register_element_cls("w:autoSpaceDE", CT_OnOff)
register_element_cls("w:autoSpaceDN", CT_OnOff)
register_element_cls("w:bidi", CT_OnOff)
register_element_cls("w:adjustRightInd", CT_OnOff)
register_element_cls("w:snapToGrid", CT_OnOff)
register_element_cls("w:ind", CT_Ind)
register_element_cls("w:contextualSpacing", CT_OnOff)
register_element_cls("w:mirrorIndents", CT_OnOff)
register_element_cls("w:suppressOverlap", CT_OnOff)
register_element_cls("w:jc", CT_Jc)
register_element_cls("w:textDirection", CT_TextDirection)
register_element_cls("w:textAlignment", CT_TextAlignment)
register_element_cls("w:textboxTightWrap", CT_TextboxTightWrap)
register_element_cls("w:outlineLvl", CT_DecimalNumber)
register_element_cls("w:divId", CT_DecimalNumber)
register_element_cls("w:cnfStyle", CT_Cnf)

from .text.num_props import CT_NumPr, CT_TrackChangeNumbering

register_element_cls("w:numPr", CT_NumPr)
register_element_cls("w:ilvl", CT_DecimalNumber)
register_element_cls("w:numId", CT_DecimalNumber)
register_element_cls("w:numberingChange", CT_TrackChangeNumbering)
register_element_cls("w:ins", CT_TrackChange)


from .text.hyperlink import CT_Hyperlink

register_element_cls("w:hyperlink", CT_Hyperlink)

from .text.run import CT_R, CT_T

register_element_cls("w:r", CT_R)
register_element_cls("w:t", CT_T)

from .text.run_props import (
    CT_RPr,
    CT_RPrChange,
    CT_Underline,
    CT_VerticalAlignRun,
)

register_element_cls("w:rPr", CT_RPr)
register_element_cls("w:rPrChange", CT_RPrChange)
register_element_cls("w:i", CT_OnOff)
register_element_cls("w:iCs", CT_OnOff)
register_element_cls("w:b", CT_OnOff)
register_element_cls("w:bCs", CT_OnOff)
register_element_cls("w:caps", CT_OnOff)
register_element_cls("w:smallCaps", CT_OnOff)
register_element_cls("w:strike", CT_OnOff)
register_element_cls("w:dstrike", CT_OnOff)
register_element_cls("w:outline", CT_OnOff)
register_element_cls("w:shadow", CT_OnOff)
register_element_cls("w:emboss", CT_OnOff)
register_element_cls("w:imprint", CT_OnOff)
register_element_cls("w:noProof", CT_OnOff)
register_element_cls("w:snapToGrid", CT_OnOff)
register_element_cls("w:vanish", CT_OnOff)
register_element_cls("w:webHidden", CT_OnOff)
register_element_cls("w:rStyle", CT_String)
register_element_cls("w:rFonts", CT_Fonts)
register_element_cls("w:color", CT_Color)
register_element_cls("w:w", CT_TextScale)
register_element_cls("w:kern", CT_HpsMeasure)
register_element_cls("w:position", CT_SignedHpsMeasure)
register_element_cls("w:sz", CT_HpsMeasure)
register_element_cls("w:szCs", CT_HpsMeasure)
register_element_cls("w:highlight", CT_Highlight)
register_element_cls("w:u", CT_Underline)
register_element_cls("w:effect", CT_TextEffect)
register_element_cls("w:bdr", CT_Border)
register_element_cls("w:shd", CT_Shd)
register_element_cls("w:fitText", CT_FitText)
register_element_cls("w:vertAlign", CT_VerticalAlignRun)
register_element_cls("w:rtl", CT_OnOff)
register_element_cls("w:cs", CT_OnOff)
register_element_cls("w:em", CT_Em)
register_element_cls("w:lang", CT_Language)
register_element_cls("w:eastAsianLayout", CT_EastAsianLayout)
register_element_cls("w:specVanish", CT_OnOff)
register_element_cls("w:oMath", CT_OnOff)

from .table.table import CT_Row, CT_Tbl, CT_Tc

register_element_cls("w:tbl", CT_Tbl)
register_element_cls("w:tr", CT_Row)
register_element_cls("w:tc", CT_Tc)

from .table.table_props import CT_TblPr

register_element_cls("w:tblPr", CT_TblPr)
register_element_cls("w:tblStyle", CT_String)

from .table.row_props import CT_TrPr

register_element_cls("w:trPr", CT_TrPr)


from .table.cell_props import (
    CT_HMerge,
    CT_TblWidth,
    CT_TcBorders,
    CT_TcMar,
    CT_TcPr,
    CT_VerticalJc,
    CT_VMerge,
)

register_element_cls("w:tcPr", CT_TcPr)
register_element_cls("w:tcW", CT_TblWidth)
register_element_cls("w:gridSpan", CT_DecimalNumber)
register_element_cls("w:hMerge", CT_HMerge)
register_element_cls("w:vMerge", CT_VMerge)
register_element_cls("w:tcBorders", CT_TcBorders)
register_element_cls("w:noWrap", CT_OnOff)
register_element_cls("w:tcMar", CT_TcMar)
register_element_cls("w:tcFitText", CT_OnOff)
register_element_cls("w:vAlign", CT_VerticalJc)
register_element_cls("w:hideMark", CT_OnOff)

from .styles import (
    CT_DocDefaults,
    CT_LatentStyles,
    CT_RPrDefault,
    CT_Style,
    CT_Styles,
    CT_TblStylePr,
)

register_element_cls("w:docDefaults", CT_DocDefaults)
register_element_cls("w:rPrDefault", CT_RPrDefault)

register_element_cls("w:styles", CT_Styles)

register_element_cls("w:latentStyles", CT_LatentStyles)

register_element_cls("w:style", CT_Style)
register_element_cls("w:aliases", CT_String)
register_element_cls("w:basedOn", CT_String)
register_element_cls("w:next", CT_String)
register_element_cls("w:link", CT_String)
register_element_cls("w:autoRedefine", CT_String)
register_element_cls("w:hidden", CT_OnOff)
register_element_cls("w:uiPriority", CT_DecimalNumber)
register_element_cls("w:semiHidden", CT_OnOff)
register_element_cls("w:unhideWhenUsed", CT_OnOff)
register_element_cls("w:qFormat", CT_OnOff)
register_element_cls("w:locked", CT_OnOff)
register_element_cls("w:personal", CT_OnOff)
register_element_cls("w:personalCompose", CT_OnOff)
register_element_cls("w:personalReply", CT_OnOff)
register_element_cls("w:tblStylePr", CT_TblStylePr)

from .numbering import (
    CT_AbstractNum,
    CT_LevelSuffix,
    CT_LevelText,
    CT_Lvl,
    CT_LvlLegacy,
    CT_MultiLevelType,
    CT_Num,
    CT_Numbering,
    CT_NumFmt,
    CT_NumLvl,
    CT_NumPicBullet,
)

register_element_cls("w:numbering", CT_Numbering)
register_element_cls("w:numPicBullet", CT_NumPicBullet)

register_element_cls("w:abstractNum", CT_AbstractNum)
register_element_cls("w:numIdMacAtCleanup", CT_DecimalNumber)
register_element_cls("w:abstractNumId", CT_DecimalNumber)
register_element_cls("w:lvlOverride", CT_NumLvl)
register_element_cls("w:startOverride", CT_DecimalNumber)
register_element_cls("w:nsid", CT_LongHexNumber)
register_element_cls("w:multiLevelType", CT_MultiLevelType)
register_element_cls("w:tmpl", CT_LongHexNumber)
register_element_cls("w:styleLink", CT_String)
register_element_cls("w:numStyleLink", CT_String)

register_element_cls("w:num", CT_Num)
register_element_cls("w:lvl", CT_Lvl)
register_element_cls("w:start", CT_DecimalNumber)
register_element_cls("w:numFmt", CT_NumFmt)
register_element_cls("w:lvlRestart", CT_DecimalNumber)
register_element_cls("w:isLgl", CT_OnOff)
register_element_cls("w:suff", CT_LevelSuffix)
register_element_cls("w:lvlText", CT_LevelText)
register_element_cls("w:lvlPicBulletId", CT_DecimalNumber)
register_element_cls("w:legacy", CT_LvlLegacy)
register_element_cls("w:lvlJc", CT_Jc)
