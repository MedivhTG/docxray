from functools import cached_property

# docxray stuff
from docxray.xsd.primitives import XsdToken

from .ns import PIC, WP, A, NoNS, R
from .st.dml_main import ST_PositiveCoordinate
from .st.dml_wordprocessing_drawing import ST_WrapDistance
from .xmlchemy import OxmlElement


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


class CT_NonVisualPictureProperties(OxmlElement):
    pass


class CT_PictureNonVisual(OxmlElement):
    @cached_property
    def nvPicPr(self) -> CT_NonVisualDrawingProps:
        return self.child_exactly_one(PIC.NV_PIC_PR, CT_NonVisualDrawingProps)

    @cached_property
    def cNvPicPr(self) -> CT_NonVisualPictureProperties:
        return self.child_exactly_one(
            PIC.C_NV_PIC_PR, CT_NonVisualPictureProperties
        )


class CT_Blip(OxmlElement):
    @cached_property
    def embed(self) -> str:
        return self.attr_optional(R.EMBED, default="")


class CT_BlipFillProperties(OxmlElement):
    @cached_property
    def blip(self) -> CT_Blip | None:
        return self.child_zero_or_one(A.BLIP, CT_Blip)


class CT_ShapeProperties(OxmlElement):
    pass


class CT_Picture(OxmlElement):
    @cached_property
    def nvPicPr(self) -> CT_PictureNonVisual:
        return self.child_exactly_one(PIC.NV_PIC_PR, CT_PictureNonVisual)

    @cached_property
    def blipFill(self) -> CT_BlipFillProperties:
        return self.child_exactly_one(PIC.BLIP_FILL, CT_BlipFillProperties)

    @cached_property
    def spPr(self) -> CT_ShapeProperties:
        return self.child_exactly_one(PIC.SP_PR, CT_ShapeProperties)


class CT_GraphicalObjectData(OxmlElement):
    # In xsd schema we see `unnbounded` maxOccurs, but in reality it's not
    @cached_property
    def pic(self) -> CT_Picture | None:
        return self.child_zero_or_one(PIC.PIC, CT_Picture)


class CT_GraphicalObject(OxmlElement):
    @cached_property
    def uri(self) -> str:
        return self.attr_required(NoNS.URI, XsdToken)

    @cached_property
    def graphicData(self) -> CT_GraphicalObjectData:
        return self.child_exactly_one(A.GRAPHIC_DATA, CT_GraphicalObjectData)


class CT_Anchor(OxmlElement):
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
