from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

# docxray stuff
from docxray.oxml.t.ns import R, W
from docxray.oxml.t.st.enums import SE_ON_OFF_1
from docxray.oxml.t.st.shared_common import ST_OnOff, ST_String
from docxray.oxml.t.st.shared_rel_ref import ST_RelationshipId
from docxray.oxml.t.xmlchemy import OxmlElement

if TYPE_CHECKING:
    from .paragraph import EG_PContent


class CT_Hyperlink(OxmlElement):
    @cached_property
    def inner_content_elements(self) -> list[EG_PContent]:
        from .paragraph import XPATH_P_CONTENT

        return self.xpath(XPATH_P_CONTENT)

    @cached_property
    def tgtFrame(self) -> str | None:
        return self.attr_optional(W.TGT_FRAME, ST_String)

    @cached_property
    def tooltip(self) -> str | None:
        return self.attr_optional(W.TOOLTIP, ST_String)

    @cached_property
    def docLocation(self) -> str | None:
        return self.attr_optional(W.DOC_LOCATION, ST_String)

    @cached_property
    def history(self) -> bool | SE_ON_OFF_1 | None:
        return self.attr_optional(W.HISTORY, ST_OnOff)

    @cached_property
    def anchor(self) -> str | None:
        return self.attr_optional(W.ANCHOR, ST_String)

    @cached_property
    def id(self) -> str | None:
        return self.attr_optional(R.ID, ST_RelationshipId)
