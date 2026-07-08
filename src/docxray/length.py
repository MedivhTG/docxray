from __future__ import annotations

from typing import Self


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
