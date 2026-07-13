from functools import cached_property
from typing import Any

# docxray stuff
from docxray.oxml.t.drawing import CT_Drawing
from docxray.oxml.t.ns import W
from docxray.oxml.t.proxy.base import ElementProxy
from docxray.oxml.t.proxy.drawing import Drawing
from docxray.oxml.t.shared import CT_Empty
from docxray.oxml.t.st.enums import SE_BR_CLEAR, SE_BR_TYPE
from docxray.oxml.t.text.run import CT_Br, CT_PTab, CT_Text, EG_RunInnerContent

type RunInnerContent = TxtFragment | Drawing | Break | Tab


def run_inner_content(
    item: EG_RunInnerContent, instance: Any
) -> RunInnerContent | None:
    if isinstance(item, CT_Text):
        if item.tag_name == "t":
            return TxtFragment(item, instance)
    elif isinstance(item, CT_Drawing):
        return Drawing(item, instance)
    elif isinstance(item, CT_Br):
        return Break(item, instance)
    # TODO: extend
    elif isinstance(item, CT_PTab):
        return None
    # TODO: extend
    elif isinstance(item, CT_Empty):
        if item.tag == W.TAB:
            return Tab(item, instance)
    return None


class Tab(ElementProxy[CT_Empty]):
    pass


class Break(ElementProxy[CT_Br]):
    @cached_property
    def break_type(self) -> SE_BR_TYPE:
        if self.element.type is None:
            return SE_BR_TYPE.TEXT_WRAPPING
        return self.element.type

    @cached_property
    def how_wrap(self) -> SE_BR_CLEAR:
        if self.break_type != SE_BR_TYPE.TEXT_WRAPPING:
            return SE_BR_CLEAR.NONE
        if self.element.clear_attr is None:
            return SE_BR_CLEAR.NONE
        return self.element.clear_attr


class TxtFragment(ElementProxy[CT_Text]):
    @cached_property
    def raw(self) -> str:
        """Text inside of txt tag `as-is`."""
        return self._element.txt

    @cached_property
    def preserve(self) -> bool:
        """Preserve space chars inside of txt tag or not."""
        return self.element.space == "preserve"
