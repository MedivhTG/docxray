"""Objects shared by docx modules."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    import docx.types as t
    from docx.opc.part import XmlPart
    from docx.oxml.xmlchemy import BaseOxmlElement
    from docx.parts.story import StoryPart


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

    def __new__(cls, emu: int):
        return int.__new__(cls, emu)

    @property
    def cm(self):
        """The equivalent length expressed in centimeters (float)."""
        return self / float(self._EMUS_PER_CM)

    @property
    def emu(self):
        """The equivalent length expressed in English Metric Units (int)."""
        return self

    @property
    def inches(self):
        """The equivalent length expressed in inches (float)."""
        return self / float(self._EMUS_PER_INCH)

    @property
    def mm(self):
        """The equivalent length expressed in millimeters (float)."""
        return self / float(self._EMUS_PER_MM)

    @property
    def pt(self):
        """Floating point length in points."""
        return self / float(self._EMUS_PER_PT)

    @property
    def twips(self):
        """The equivalent length expressed in twips (int)."""
        return int(round(self / float(self._EMUS_PER_TWIP)))


class Inches(Length):
    """Convenience constructor for length in inches, e.g. ``width = Inches(0.5)``."""

    def __new__(cls, inches: float):
        emu = int(inches * Length._EMUS_PER_INCH)
        return Length.__new__(cls, emu)


class Cm(Length):
    """Convenience constructor for length in centimeters, e.g. ``height = Cm(12)``."""

    def __new__(cls, cm: float):
        emu = int(cm * Length._EMUS_PER_CM)
        return Length.__new__(cls, emu)


class Emu(Length):
    """Convenience constructor for length in English Metric Units, e.g. ``width =
    Emu(457200)``."""

    def __new__(cls, emu: int):
        return Length.__new__(cls, int(emu))


class Mm(Length):
    """Convenience constructor for length in millimeters, e.g. ``width = Mm(240.5)``."""

    def __new__(cls, mm: float):
        emu = int(mm * Length._EMUS_PER_MM)
        return Length.__new__(cls, emu)


class Pt(Length):
    """Convenience value class for specifying a length in points."""

    def __new__(cls, points: float):
        emu = int(points * Length._EMUS_PER_PT)
        return Length.__new__(cls, emu)


class Twips(Length):
    """Convenience constructor for length in twips, e.g. ``width = Twips(42)``.

    A twip is a twentieth of a point, 635 EMU.
    """

    def __new__(cls, twips: float):
        emu = int(twips * Length._EMUS_PER_TWIP)
        return Length.__new__(cls, emu)


ELM_T = TypeVar("ELM_T", bound=BaseOxmlElement)


class ElementProxy(Generic[ELM_T]):
    """Base class for lxml element proxy classes.

    An element proxy class is one whose primary responsibilities are fulfilled by
    manipulating the attributes and child elements of an XML element. They are the most
    common type of class in python-docx other than custom element (oxml) classes.
    """

    def __init__(
        self, element: ELM_T, parent: t.ProvidesXmlPart | None = None
    ):
        self._element = element
        self._parent = parent

    @property
    def element(self) -> ELM_T:
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self) -> XmlPart:
        """The package part containing this object."""
        if self._parent is None:
            raise ValueError("part is not accessible from this element")
        return self._parent.part


class Parented:
    """Provides common services for document elements that occur below a part but may
    occasionally require an ancestor object to provide a service, such as add or drop a
    relationship.

    Provides ``self._parent`` attribute to subclasses.
    """

    def __init__(self, parent: t.ProvidesXmlPart):
        self._parent = parent

    @property
    def part(self) -> XmlPart:
        """The package part containing this object."""
        return self._parent.part


class StoryChild:
    """A document element within a story part.

    Story parts include DocumentPart and Header/FooterPart and can contain block items
    (paragraphs and tables). Items from the block-item subtree occasionally require an
    ancestor object to provide access to part-level or package-level items like styles
    or images or to add or drop a relationship.

    Provides `self._parent` attribute to subclasses.
    """

    def __init__(self, parent: t.ProvidesStoryPart):
        self._parent = parent

    @property
    def part(self) -> StoryPart:
        """The package part containing this object."""
        return self._parent.part
