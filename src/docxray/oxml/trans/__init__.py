"""Here CT_* classes mapped in memory for lxml namepsace class lookup."""

# ruff: noqa: E402

from .document import CT_Body, CT_Document
from .parser import register_element_cls
from .shared import (
    CT_Border,
    CT_Cnf,
    CT_Color,
    CT_DecimalNumber,
    CT_EastAsianLayout,
    CT_Em,
    CT_Empty,
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
    CT_TblWidth,
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

from .text.omath import CT_OMath, CT_OMathJc, CT_OMathPara, CT_OMathParaPr

register_element_cls("m:oMathPara", CT_OMathPara)
register_element_cls("m:oMathParaPr", CT_OMathParaPr)
register_element_cls("m:jc", CT_OMathJc)
register_element_cls("m:oMath", CT_OMath)

from .text.omath_elm import (
    CT_D,
    CT_F,
    CT_M,
    CT_MC,
    CT_MCS,
    CT_MR,
    CT_RPR,
    CT_Acc,
    CT_AccPr,
    CT_Bar,
    CT_BarPr,
    CT_BorderBox,
    CT_BorderBoxPr,
    CT_Box,
    CT_BoxPr,
    CT_Char,
    CT_CtrlPr,
    CT_DPr,
    CT_EqArr,
    CT_EqArrPr,
    CT_FPr,
    CT_FType,
    CT_Func,
    CT_FuncPr,
    CT_GroupChr,
    CT_GroupChrPr,
    CT_Integer2,
    CT_Integer255,
    CT_LimLoc,
    CT_LimLow,
    CT_LimLowPr,
    CT_LimUpp,
    CT_LimUppPr,
    CT_ManualBreak,
    CT_MCPr,
    CT_MPr,
    CT_Nary,
    CT_NaryPr,
    CT_OMathArg,
    CT_OMathArgPr,
    CT_Phant,
    CT_PhantPr,
    CT_R_OMath,
    CT_Rad,
    CT_RadPr,
    CT_Script,
    CT_Shp,
    CT_SpacingRule,
    CT_SPre,
    CT_SPrePr,
    CT_SSub,
    CT_SSubPr,
    CT_SSubSup,
    CT_SSubSupPr,
    CT_SSup,
    CT_SSupPr,
    CT_Style_OMath,
    CT_Text_OMath,
    CT_TopBot,
    CT_UnSignedInteger,
    CT_XAlign,
    CT_YAlign,
)

register_element_cls("m:e", CT_OMathArg)
register_element_cls("m:argPr", CT_OMathArgPr)
register_element_cls("m:argSz", CT_Integer2)

register_element_cls("m:acc", CT_Acc)
register_element_cls("m:accPr", CT_AccPr)

register_element_cls("m:chr", CT_Char)
register_element_cls("m:ctrlPr", CT_CtrlPr)

register_element_cls("m:bar", CT_Bar)
register_element_cls("m:barPr", CT_BarPr)
register_element_cls("m:pos", CT_TopBot)

register_element_cls("m:box", CT_Box)
register_element_cls("m:boxPr", CT_BoxPr)
register_element_cls("m:opEmu", CT_OnOff)
register_element_cls("m:noBreak", CT_OnOff)
register_element_cls("m:diff", CT_OnOff)
register_element_cls("m:brk", CT_ManualBreak)
register_element_cls("m:aln", CT_OnOff)

register_element_cls("m:borderBox", CT_BorderBox)
register_element_cls("m:borderBoxPr", CT_BorderBoxPr)
register_element_cls("m:hideTop", CT_OnOff)
register_element_cls("m:hideBot", CT_OnOff)
register_element_cls("m:hideLeft", CT_OnOff)
register_element_cls("m:hideRight", CT_OnOff)
register_element_cls("m:strikeH", CT_OnOff)
register_element_cls("m:strikeV", CT_OnOff)
register_element_cls("m:strikeBLTR", CT_OnOff)
register_element_cls("m:strikeTLBR", CT_OnOff)

register_element_cls("m:d", CT_D)
register_element_cls("m:dPr", CT_DPr)
register_element_cls("m:begChr", CT_Char)
register_element_cls("m:sepChr", CT_Char)
register_element_cls("m:endChr", CT_Char)
register_element_cls("m:grow", CT_OnOff)
register_element_cls("m:shp", CT_Shp)

register_element_cls("m:eqArr", CT_EqArr)
register_element_cls("m:eqArrPr", CT_EqArrPr)
register_element_cls("m:baseJc", CT_YAlign)
register_element_cls("m:maxDist", CT_OnOff)
register_element_cls("m:objDist", CT_OnOff)
register_element_cls("m:rSpRule", CT_SpacingRule)
register_element_cls("m:rSp", CT_UnSignedInteger)

register_element_cls("m:f", CT_F)
register_element_cls("m:fPr", CT_FPr)
register_element_cls("m:type", CT_FType)
register_element_cls("m:num", CT_OMathArg)
register_element_cls("m:den", CT_OMathArg)

register_element_cls("m:func", CT_Func)
register_element_cls("m:funcPr", CT_FuncPr)
register_element_cls("m:fName", CT_OMathArg)

register_element_cls("m:groupChr", CT_GroupChr)
register_element_cls("m:groupChrPr", CT_GroupChrPr)
register_element_cls("m:vertJc", CT_TopBot)

register_element_cls("m:limLow", CT_LimLow)
register_element_cls("m:limLowPr", CT_LimLowPr)
register_element_cls("m:lim", CT_OMathArg)

register_element_cls("m:limUpp", CT_LimUpp)
register_element_cls("m:limUppPr", CT_LimUppPr)

register_element_cls("m:m", CT_M)
register_element_cls("m:mPr", CT_MPr)
register_element_cls("m:plcHide", CT_OnOff)
register_element_cls("m:cGpRule", CT_SpacingRule)
register_element_cls("m:cSp", CT_UnSignedInteger)
register_element_cls("m:cGp", CT_UnSignedInteger)
register_element_cls("m:mcs", CT_MCS)
register_element_cls("m:mr", CT_MR)

register_element_cls("m:mc", CT_MC)
register_element_cls("m:mcPr", CT_MCPr)
register_element_cls("m:count", CT_Integer255)
register_element_cls("m:mcJc", CT_XAlign)

register_element_cls("m:nary", CT_Nary)
register_element_cls("m:naryPr", CT_NaryPr)
register_element_cls("m:limLoc", CT_LimLoc)
register_element_cls("m:subHide", CT_OnOff)
register_element_cls("m:supHide", CT_OnOff)
register_element_cls("m:sub", CT_OMathArg)
register_element_cls("m:sup", CT_OMathArg)

register_element_cls("m:phant", CT_Phant)
register_element_cls("m:phantPr", CT_PhantPr)
register_element_cls("m:show", CT_OnOff)
register_element_cls("m:zeroWid", CT_OnOff)
register_element_cls("m:zeroAsc", CT_OnOff)
register_element_cls("m:zeroDesc", CT_OnOff)
register_element_cls("m:transp", CT_OnOff)

register_element_cls("m:rad", CT_Rad)
register_element_cls("m:radPr", CT_RadPr)
register_element_cls("m:degHide", CT_OnOff)
register_element_cls("m:deg", CT_OMathArg)

register_element_cls("m:sPre", CT_SPre)
register_element_cls("m:sPrePr", CT_SPrePr)

register_element_cls("m:sSub", CT_SSub)
register_element_cls("m:sSubPr", CT_SSubPr)

register_element_cls("m:sSubSup", CT_SSubSup)
register_element_cls("m:sSubSupPr", CT_SSubSupPr)
register_element_cls("m:alnScr", CT_OnOff)

register_element_cls("m:sSup", CT_SSup)
register_element_cls("m:sSupPr", CT_SSupPr)

register_element_cls("m:r", CT_R_OMath)
register_element_cls("m:rPr", CT_RPR)
register_element_cls("m:lit", CT_OnOff)
register_element_cls("m:nor", CT_OnOff)
register_element_cls("m:scr", CT_Script)
register_element_cls("m:sty", CT_Style_OMath)
register_element_cls("m:t", CT_Text_OMath)

from .text.paragraph_props import (
    CT_Ind,
    CT_PBdr,
    CT_PPr,
    CT_Spacing,
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
register_element_cls("w:spacing", CT_Spacing)
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

from .text.run import CT_R, CT_Br, CT_PTab, CT_Sym, CT_Text

register_element_cls("w:r", CT_R)
register_element_cls("w:br", CT_Br)
register_element_cls("w:noBreakHyphen", CT_Empty)
register_element_cls("w:softHyphen", CT_Empty)
register_element_cls("w:sym", CT_Sym)
register_element_cls("w:cr", CT_Empty)
register_element_cls("w:tab", CT_Empty)
register_element_cls("w:ptab", CT_PTab)
register_element_cls("w:t", CT_Text)

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

from .table.table_props import (
    CT_TblBorders,
    CT_TblCellMar,
    CT_TblLayoutType,
    CT_TblLook,
    CT_TblOverlap,
    CT_TblPPr,
    CT_TblPr,
)

register_element_cls("w:tblPr", CT_TblPr)
register_element_cls("w:tblStyle", CT_String)
register_element_cls("w:tblpPr", CT_TblPPr)
register_element_cls("w:tblOverlap", CT_TblOverlap)
register_element_cls("w:bidiVisual", CT_OnOff)
register_element_cls("w:tblStyleRowBandSize", CT_DecimalNumber)
register_element_cls("w:tblStyleColBandSize", CT_DecimalNumber)
register_element_cls("w:tblW", CT_TblWidth)
register_element_cls("w:tblCellSpacing", CT_TblWidth)
register_element_cls("w:tblInd", CT_TblWidth)
register_element_cls("w:tblBorders", CT_TblBorders)
register_element_cls("w:tblLayout", CT_TblLayoutType)
register_element_cls("w:tblCellMar", CT_TblCellMar)
register_element_cls("w:tblLook", CT_TblLook)
register_element_cls("w:tblCaption", CT_String)
register_element_cls("w:tblDescription", CT_String)

from .table.row_props import CT_Height, CT_TblPrEx, CT_TrPr

register_element_cls("w:trPr", CT_TrPr)
register_element_cls("w:trHeight", CT_Height)
register_element_cls("w:tblPrEx", CT_TblPrEx)


from .table.cell_props import (
    CT_HMerge,
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
register_element_cls("w:tcMar", CT_TcMar)

register_element_cls("w:tcBorders", CT_TcBorders)
register_element_cls("w:top", CT_Border)
register_element_cls("w:left", CT_Border)
register_element_cls("w:bottom", CT_Border)
register_element_cls("w:right", CT_Border)
register_element_cls("w:insideH", CT_Border)
register_element_cls("w:insideV", CT_Border)
register_element_cls("w:tl2br", CT_Border)
register_element_cls("w:tr2bl", CT_Border)

register_element_cls("w:noWrap", CT_OnOff)
register_element_cls("w:tcMar", CT_TcMar)
register_element_cls("w:tcFitText", CT_OnOff)
register_element_cls("w:vAlign", CT_VerticalJc)
register_element_cls("w:hideMark", CT_OnOff)


from .drawing import (
    CT_Anchor,
    CT_Blip,
    CT_BlipFillProperties,
    CT_Drawing,
    CT_GraphicalObject,
    CT_GraphicalObjectData,
    CT_Inline,
    CT_NonVisualDrawingProps,
    CT_NonVisualGraphicFrameProperties,
    CT_NonVisualPictureProperties,
    CT_Picture,
    CT_PictureNonVisual,
    CT_PositiveSize2D,
    CT_ShapeProperties,
)

register_element_cls("w:drawing", CT_Drawing)

register_element_cls("wp:anchor", CT_Anchor)

register_element_cls("wp:inline", CT_Inline)
register_element_cls("wp:extent", CT_PositiveSize2D)
register_element_cls("wp:docPr", CT_NonVisualDrawingProps)
register_element_cls(
    "wp:cNvGraphicFramePr", CT_NonVisualGraphicFrameProperties
)
register_element_cls("a:graphic", CT_GraphicalObject)
register_element_cls("a:graphicData", CT_GraphicalObjectData)

register_element_cls("pic:pic", CT_Picture)

register_element_cls("pic:nvPicPr", CT_PictureNonVisual)
register_element_cls("pic:cNvPr", CT_NonVisualDrawingProps)
register_element_cls("pic:cNvPicPr", CT_NonVisualPictureProperties)

register_element_cls("pic:blipFill", CT_BlipFillProperties)
register_element_cls("a:blip", CT_Blip)

register_element_cls("pic:spPr", CT_ShapeProperties)

from .styles import (
    CT_DocDefaults,
    CT_LatentStyles,
    CT_PPrDefault,
    CT_RPrDefault,
    CT_Style,
    CT_Styles,
    CT_TblStylePr,
)

register_element_cls("w:docDefaults", CT_DocDefaults)
register_element_cls("w:rPrDefault", CT_RPrDefault)
register_element_cls("w:pPrDefault", CT_PPrDefault)

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

from .settings import CT_Settings

register_element_cls("w:settings", CT_Settings)
register_element_cls("w:themeFontLang", CT_Language)
