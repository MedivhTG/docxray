"""Custom element classes related to the styles part."""

from __future__ import annotations

from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import W
from docxray.oxml.trans.shared import (
    CT_DecimalNumber,
    CT_LongHexNumber,
    CT_OnOff,
    CT_String,
)
from docxray.oxml.trans.st.enums import (
    SE_StyleType,
    SE_TblStyleOverrideType,
)
from docxray.oxml.trans.st.shared_common import (
    ST_OnOff,
    ST_String,
)
from docxray.oxml.trans.st.wml import (
    ST_StyleType,
    ST_TblStyleOverrideType,
)
from docxray.oxml.trans.table.cell_props import CT_TcPr
from docxray.oxml.trans.table.row_props import CT_TrPr
from docxray.oxml.trans.table.table_props import CT_TblPr
from docxray.oxml.trans.text.paragraph_props import CT_PPr
from docxray.oxml.trans.text.run_props import CT_RPr
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_RPrDefault(OxmlElement):
    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)


class CT_DocDefaults(OxmlElement):
    @cached_property
    def rPrDefault(self) -> CT_RPrDefault | None:
        return self.child_zero_or_one(W.R_PR_DEFAULT, CT_RPrDefault)


class CT_LatentStyles(OxmlElement):
    pass


class CT_TblStylePr(OxmlElement):
    @cached_property
    def type(self) -> SE_TblStyleOverrideType:
        return self.attr_required(W.TYPE, ST_TblStyleOverrideType)

    @cached_property
    def pPr(self) -> CT_PPr | None:
        return self.child_zero_or_one(W.P_PR, CT_PPr)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def tblPr(self) -> CT_TblPr | None:
        return self.child_zero_or_one(W.TBL_PR, CT_TblPr)

    @cached_property
    def trPr(self) -> CT_TrPr | None:
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)

    @cached_property
    def tcPr(self) -> CT_TcPr | None:
        return self.child_zero_or_one(W.TC_PR, CT_TcPr)


class CT_Style(OxmlElement):
    """A ``<w:style>`` element, representing a style definition."""

    @cached_property
    def type(self) -> SE_StyleType | None:
        return self.attr_optional(W.TYPE, ST_StyleType, SE_StyleType.PARAGRAPH)

    @cached_property
    def styleId(self) -> str | None:
        return self.attr_optional(W.STYLE_ID, ST_String)

    @cached_property
    def default(self) -> bool | None:
        return self.attr_optional(W.DEFAULT, ST_OnOff)

    @cached_property
    def customStyle(self) -> bool | None:
        return self.attr_optional(W.CUSTOM_STYLE, ST_OnOff)

    @cached_property
    def name(self) -> CT_String | None:
        """Primary style name."""
        return self.child_zero_or_one(W.NAME, CT_String)

    @cached_property
    def aliases(self) -> CT_String | None:
        """Alternate style names."""
        return self.child_zero_or_one(W.ALIASES, CT_String)

    @cached_property
    def basedOn(self) -> CT_String | None:
        """Parent style ID."""
        return self.child_zero_or_one(W.BASED_ON, CT_String)

    @cached_property
    def next(self) -> CT_String | None:
        return self.child_zero_or_one(W.NEXT, CT_String)

    @cached_property
    def link(self) -> CT_String | None:
        """Linked style reference."""
        return self.child_zero_or_one(W.LINK, CT_String)

    @cached_property
    def autoRedefine(self) -> CT_OnOff | None:
        """Automatically merge user formatting into style definition."""
        return self.child_zero_or_one(W.AUTO_REDEFINE, CT_OnOff)

    @cached_property
    def hidden(self) -> CT_OnOff | None:
        """Hide style from user interface."""
        return self.child_zero_or_one(W.HIDDEN, CT_OnOff)

    @cached_property
    def uiPriority(self) -> CT_DecimalNumber | None:
        """Optional user interface sorting order."""
        return self.child_zero_or_one(W.UI_PRIORITY, CT_DecimalNumber)

    @cached_property
    def semiHidden(self) -> CT_OnOff | None:
        """Hide style from main user interface."""
        return self.child_zero_or_one(W.SEMI_HIDDEN, CT_OnOff)

    @cached_property
    def unhideWhenUsed(self) -> CT_OnOff | None:
        """Remove semi-hidden property when style is used."""
        return self.child_zero_or_one(W.UNHIDE_WHEN_USED, CT_OnOff)

    @cached_property
    def qFormat(self) -> CT_OnOff | None:
        """Primary style."""
        return self.child_zero_or_one(W.Q_FORMAT, CT_OnOff)

    @cached_property
    def locked(self) -> CT_OnOff | None:
        """Style cannot be applied."""
        return self.child_zero_or_one(W.LOCKED, CT_OnOff)

    @cached_property
    def personal(self) -> CT_OnOff | None:
        """E-mail message text style."""
        return self.child_zero_or_one(W.PERSONAL, CT_OnOff)

    @cached_property
    def personalCompose(self) -> CT_OnOff | None:
        """E-mail message composition style."""
        return self.child_zero_or_one(W.PERSONAL_COMPOSE, CT_OnOff)

    @cached_property
    def personalReply(self) -> CT_OnOff | None:
        """E-mail message reply style."""
        return self.child_zero_or_one(W.PERSONAL_REPLY, CT_OnOff)

    @cached_property
    def rsid(self) -> CT_LongHexNumber | None:
        """Revision identifier for style definition."""
        return self.child_zero_or_one(W.RSID, CT_LongHexNumber)

    @cached_property
    def pPr(self) -> CT_PPr | None:
        """Style paragraph properties."""
        return self.child_zero_or_one(W.P_PR, CT_PPr)

    @cached_property
    def rPr(self) -> CT_RPr | None:
        """Run properties."""
        return self.child_zero_or_one(W.R_PR, CT_RPr)

    @cached_property
    def tblPr(self) -> CT_TblPr | None:
        """Style table properties."""
        return self.child_zero_or_one(W.TBL_PR, CT_TblPr)

    @cached_property
    def trPr(self) -> CT_TrPr | None:
        """Style table row properties."""
        return self.child_zero_or_one(W.TR_PR, CT_TrPr)

    @cached_property
    def tcPr(self) -> CT_TcPr | None:
        """Style table cell properties."""
        return self.child_zero_or_one(W.TC_PR, CT_TcPr)

    @cached_property
    def tblStylePr_lst(self) -> list[CT_TblStylePr]:
        return self.child_zero_or_more(W.TBL_STYLE_PR, CT_TblStylePr)

    def tblStylePr_for(
        self, type: SE_TblStyleOverrideType
    ) -> CT_TblStylePr | None:
        tblStylPr_elm = self.find(
            f"./{W.TBL_STYLE_PR}[@{W.TYPE}='{type}']", CT_TblStylePr
        )
        if tblStylPr_elm is None:
            return None
        return tblStylPr_elm


class CT_Styles(OxmlElement):
    """``<w:styles>`` element, the root element of a styles part, i.e. styles.xml."""

    @cached_property
    def docDefaults(self) -> CT_DocDefaults | None:
        return self.child_zero_or_one(W.DOC_DEFAULTS, CT_DocDefaults)

    @cached_property
    def latentStyles_lst(self) -> list[CT_LatentStyles]:
        return self.child_zero_or_more(W.LATENT_STYLES, CT_LatentStyles)

    @cached_property
    def style_lst(self) -> list[CT_Style]:
        return self.child_zero_or_more(W.STYLE, CT_Style)

    def get_by_id(self, styleId: str) -> CT_Style | None:
        """`w:style` child where @styleId = `styleId`.

        |None| if not found.
        """
        return self.find(f"{W.STYLE}[@{W.STYLE_ID}='{styleId}']", CT_Style)
