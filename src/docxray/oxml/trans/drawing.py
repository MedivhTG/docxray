from functools import cached_property

# docxray stuff
from docxray.oxml.trans.ns import WP, A, NoNS
from docxray.oxml.trans.st.dml_main import ST_PositiveCoordinate
from docxray.oxml.trans.st.dml_wordprocessing_drawing import ST_WrapDistance
from docxray.oxml.trans.xmlchemy import OxmlElement


class CT_PositiveSize2D(OxmlElement):
    @cached_property
    def cx(self) -> int:
        return self.attr_required(NoNS.CX, ST_PositiveCoordinate)

    @cached_property
    def cy(self) -> int:
        return self.attr_required(NoNS.CY, ST_PositiveCoordinate)


class CT_NonVisualDrawingProps(OxmlElement):
    pass


class CT_NonVisualGraphicFrameProperties(OxmlElement):
    pass


class CT_EffectExtent(OxmlElement):
    pass


class CT_GraphicalObject(OxmlElement):
    pass


class CT_Anchor(OxmlElement):
    pass


class CT_Inline(OxmlElement):
    @cached_property
    def distT(self) -> int | None:
        return self.attr_optional(NoNS.DIST_T, ST_WrapDistance)

    @cached_property
    def distB(self) -> int | None:
        return self.attr_optional(NoNS.DIST_T, ST_WrapDistance)

    @cached_property
    def distL(self) -> int | None:
        return self.attr_optional(NoNS.DIST_T, ST_WrapDistance)

    @cached_property
    def distR(self) -> int | None:
        return self.attr_optional(NoNS.DIST_T, ST_WrapDistance)

    @cached_property
    def extent(self) -> CT_PositiveSize2D:
        return self.child_exactly_one(WP.EXTENT, CT_PositiveSize2D)

    @cached_property
    def effectExtent(self) -> CT_EffectExtent | None:
        return self.child_zero_or_one(WP.EFFECT_EXTENT, CT_EffectExtent)

    @cached_property
    def docPr(self) -> CT_NonVisualDrawingProps:
        return self.child_exactly_one(WP.DOC_PR, CT_NonVisualDrawingProps)

    @cached_property
    def cNvGraphicFramePr(self) -> CT_NonVisualGraphicFrameProperties | None:
        return self.child_zero_or_one(
            WP.C_NV_GRAPHIC_FRAM_PR, CT_NonVisualGraphicFrameProperties
        )

    @cached_property
    def graphic(self) -> CT_GraphicalObject:
        return self.child_exactly_one(A.GRAPHIC, CT_GraphicalObject)


class CT_Drawing(OxmlElement):
    @cached_property
    def anchor(self) -> CT_Anchor | None:
        return self.child_zero_or_one(WP.ANCHOR, CT_Anchor)

    @cached_property
    def inline(self) -> CT_Inline | None:
        return self.child_zero_or_one(WP.INLINE, CT_Inline)
