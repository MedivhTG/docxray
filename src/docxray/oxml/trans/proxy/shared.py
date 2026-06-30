"""Objects shared by docx modules."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Generic, Self, cast

# docxray stuff
from docxray.oxml.trans.parts.story import StoryPart
from docxray.oxml.trans.proxy.types import (
    ProvidesStoryPart,
    ProvidesXmlPart,
)
from docxray.oxml.trans.types import ELM_T
from docxray.transform.transformer import Transformer, TransformMethod

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.part import XmlPart
    from docxray.transform.ruleset import RuleProxy, RuleSet


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

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(
            self,
            ruleset,
            cast("RuleProxy", self.__class__.__name__),
            stringify,
            method,
        )


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

    @cached_property
    def prev_sibling(self) -> Self | None:
        sibling_list = self._element.xpath(
            f"preceding-sibling::{self._element.xml_tag_self}[1]"
        )
        if len(sibling_list) == 0:
            return None
        return self.__class__(sibling_list[0], self._parent)

    @cached_property
    def next_sibling(self) -> Self | None:
        sibling_list = self._element.xpath(
            f"following-sibling::{self._element.xml_tag_self}[1]"
        )
        if len(sibling_list) == 0:
            return None
        return self.__class__(sibling_list[0], self._parent)

    def transform(
        self,
        ruleset: RuleSet | None = None,
        stringify: bool = True,
        method: TransformMethod = "html",
    ) -> Any:
        # docxray stuff
        from docxray.oxml.trans.parts.document import DocumentPart

        ruleset = (
            ruleset or cast("DocumentPart", self.part)._default_html_ruleset
        )
        return Transformer.transform(
            self,
            ruleset,
            cast("RuleProxy", self.__class__.__name__),
            stringify,
            method,
        )


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


class NotFound:
    def __init__(self, obj: Any, path: PropertyPath) -> None:
        self.obj = obj
        self.path = path


def safe_get_prop(obj: Any, path: PropertyPath, optional: bool = True) -> Any:
    """_summary_

    Args:
        obj (Any): _description_
        path (PropertyPath): _description_
        optional (bool, optional): _description_. Defaults to True.

    Returns:
        Any: Python value or `NotFound` if property not found; or
            `optional` set to False and property was `None`.
    """
    if obj is None:
        return NotFound(obj, path)
    current = obj
    for link in path.links:
        if not hasattr(current, link):
            return NotFound(obj, path)
        current = getattr(current, link)
    if current is None:
        if optional:
            return None
        return NotFound(obj, path)
    return current


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
    _EMUS_PER_PICA = 152400

    def __new__(cls, emu: int) -> Self:
        return int.__new__(cls, emu)

    def __neg__(self) -> Length:
        """Return negative length."""
        return Length(-int(self))

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

    @property
    def pica(self) -> float:
        """The equivalent length expressed in picas (float)."""
        return self / float(self._EMUS_PER_PICA)

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


class Pica(Length):
    """Convenience constructor for length in picas (pc).

    A pica is one-sixth of an inch, 152400 EMU.
    """

    def __new__(cls, pica: float) -> Self:
        emu = int(pica * cls._EMUS_PER_PICA)
        return Length.__new__(cls, emu)
