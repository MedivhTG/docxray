"""Objects shared by docx modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Self

# docxray stuff
from docxray.oxml.trans.parts.story import StoryPart
from docxray.oxml.trans.proxy.types import (
    ProvidesStoryPart,
    ProvidesXmlPart,
)
from docxray.oxml.trans.types import ELM_T

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart


class ElementProxy(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesXmlPart) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self) -> XmlPart:
        return self._parent.part


class StoryChild(Generic[ELM_T]):
    def __init__(self, element: ELM_T, parent: ProvidesStoryPart) -> None:
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        return self._element

    @property
    def part(self) -> StoryPart:
        """The package part containing this object."""
        return self._parent.part


class PropertyPath(str):
    @property
    def prop(self) -> str:
        return self.rsplit(".", 1)[-1]

    @property
    def path_to_prop(self) -> str:
        return self.rsplit(".", 1)[0]

    @property
    def links(self) -> list[str]:
        return self.split(".")

    def join_left(self, left: str) -> PropertyPath:
        return PropertyPath.base(self.prop, f"{left}.{self.path_to_prop}")

    @classmethod
    def base(cls, prop: str, path_to_prop: str = "") -> Self:
        if not path_to_prop:
            return cls(prop)
        return cls(f"{path_to_prop}.{prop}")


def safe_get_prop(
    obj: Any, prop_path: PropertyPath, default: Any = None
) -> Any:
    """Get property from object by path safely.

    Args:
        obj (Any): From python ojbect.
        prop_path (PropertyPath): Property path like `rPr.i`
        default (Any, optional): Return default if cannot get property
            on path. Defaults to None.

    Returns:
        Any: Value from property or default.
    """
    if obj is None:
        return default
    current = obj
    for link in prop_path.links:
        if not hasattr(current, link):
            return default
        current = getattr(current, link)
    return default if current is None else current


class Length(int):
    """Base class for length constructor classes Inches, Cm, Mm, Px, and Emu.

    Behaves as an int count of English Metric Units, 914,400 to the inch, 36,000 to the
    mm. Provides convenience unit conversion methods in the form of read-only
    properties. Immutable.
    """

    _EMUS_PER_INCH = 914400
    _EMUS_PER_CM = 360000
    _EMUS_PER_MM = 36000
    _EMUS_PER_PT = 12700
    _EMUS_PER_TWIP = 635

    def __new__(cls, emu: int) -> Self:
        return int.__new__(cls, emu)

    @property
    def cm(self) -> float:
        """The equivalent length expressed in centimeters (float)."""
        return self / float(self._EMUS_PER_CM)

    @property
    def emu(self) -> Self:
        """The equivalent length expressed in English Metric Units (int)."""
        return self

    @property
    def inches(self) -> float:
        """The equivalent length expressed in inches (float)."""
        return self / float(self._EMUS_PER_INCH)

    @property
    def mm(self) -> float:
        """The equivalent length expressed in millimeters (float)."""
        return self / float(self._EMUS_PER_MM)

    @property
    def pt(self) -> float:
        """Floating point length in points."""
        return self / float(self._EMUS_PER_PT)

    @property
    def twips(self) -> int:
        """The equivalent length expressed in twips (int)."""
        return int(round(self / float(self._EMUS_PER_TWIP)))

    def px(self, dpi: int = 96) -> int:
        return int(self.inches * dpi)


class Inches(Length):
    """Convenience constructor for length in inches, e.g. ``width = Inches(0.5)``."""

    def __new__(cls, inches: float) -> Self:
        emu = int(inches * Length._EMUS_PER_INCH)
        return Length.__new__(cls, emu)


class Cm(Length):
    """Convenience constructor for length in centimeters, e.g. ``height = Cm(12)``."""

    def __new__(cls, cm: float) -> Self:
        emu = int(cm * Length._EMUS_PER_CM)
        return Length.__new__(cls, emu)


class Emu(Length):
    """Convenience constructor for length in English Metric Units, e.g. ``width =
    Emu(457200)``."""

    def __new__(cls, emu: int) -> Self:
        return Length.__new__(cls, int(emu))


class Mm(Length):
    """Convenience constructor for length in millimeters, e.g. ``width = Mm(240.5)``."""

    def __new__(cls, mm: float) -> Self:
        emu = int(mm * Length._EMUS_PER_MM)
        return Length.__new__(cls, emu)


class Pt(Length):
    """Convenience value class for specifying a length in points."""

    def __new__(cls, points: float) -> Self:
        emu = int(points * Length._EMUS_PER_PT)
        return Length.__new__(cls, emu)


class Twips(Length):
    """Convenience constructor for length in twips, e.g. ``width = Twips(42)``.

    A twip is a twentieth of a point, 635 EMU.
    """

    def __new__(cls, twips: float) -> Self:
        emu = int(twips * Length._EMUS_PER_TWIP)
        return Length.__new__(cls, emu)
