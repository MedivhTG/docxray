import re
from datetime import UTC, datetime, timedelta, timezone
from typing import Self

# Timezone: 'Z' or ±HH:MM with HH 00..13 (any MM) or exactly ±14:00.
TZ = r"(?P<tz>Z|[+-](?:0\d|1[0-3]):[0-5]\d|[+-]14:00)"
# XSD 1.1 year: at least 4 digits, optional leading '+'.
YEAR = r"\+?\d{4,}"

# Word accepts dates only in 1601..9999 (Windows FILETIME epoch .. datetime max).
MIN_YEAR = 1601
MAX_YEAR = 9999

GYEAR_RE = re.compile(rf"^(?P<y>{YEAR})(?:{TZ})?$")
GYEARMONTH_RE = re.compile(rf"^(?P<y>{YEAR})-(?P<mo>0[1-9]|1[0-2])(?:{TZ})?$")
DATE_RE = re.compile(
    rf"^(?P<y>{YEAR})-(?P<mo>0[1-9]|1[0-2])"
    rf"-(?P<d>0[1-9]|[12]\d|3[01])(?:{TZ})?$"
)
DATETIME_RE = re.compile(
    rf"^(?P<y>{YEAR})-(?P<mo>0[1-9]|1[0-2])"
    rf"-(?P<d>0[1-9]|[12]\d|3[01])"
    rf"T(?P<h>[01]\d|2[0-3]):(?P<mi>[0-5]\d):(?P<s>[0-5]\d)"
    rf"(?:\.\d{{1,6}})?{TZ}$"
)
W3CDTF_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

MIN_DATETIME = datetime(MIN_YEAR, 1, 1, 0, 0, 0, 0, tzinfo=UTC)
MAX_DATETIME = datetime(MAX_YEAR, 12, 31, 23, 59, 59, 999999, tzinfo=UTC)


class W3CDTFDateTime(datetime):
    """A ``datetime`` subclass bound to a W3C Date and Time Format value.

    Holds a parsed W3CDTF lexical form (``gYear``, ``gYearMonth``, ``date``,
    or ``dateTime``) and provides typed ``from_*`` parsers plus ``str_*``
    serializers. Missing date components in the source lexical form are
    filled with defaults (month/day = 1). The original lexical precision is
    not preserved: use the matching ``str_*`` method when writing the value
    back to XML.

    Only years in ``1601..9999`` are accepted, matching the range supported
    by Microsoft Word (the lower bound comes from the Windows ``FILETIME``
    epoch).
    """

    def str_gyear(self) -> str:
        """Serialize as an ``xs:gYear`` lexical value (``YYYY`` + optional TZ)."""
        return f"{self.year:04d}{self._format_tz()}"

    def str_gyearmonth(self) -> str:
        """Serialize as an ``xs:gYearMonth`` lexical value (``YYYY-MM`` + optional TZ)."""
        return f"{self.year:04d}-{self.month:02d}{self._format_tz()}"

    def str_date(self) -> str:
        """Serialize as an ``xs:date`` lexical value (``YYYY-MM-DD`` + optional TZ)."""
        return (
            f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
            f"{self._format_tz()}"
        )

    def str_datetime(self) -> str:
        """Serialize as an ``xs:dateTime`` lexical value in UTC with ``Z``.

        Returns:
            The value converted to UTC and formatted as
            ``YYYY-MM-DDThh:mm:ssZ``.

        Raises:
            ValueError: If the instance is timezone-naive; W3CDTF
                ``dateTime`` requires an explicit timezone.
        """
        if self.tzinfo is None:
            raise ValueError(
                "W3CDTF dateTime requires a timezone; use a tz-aware instance"
            )
        return self.astimezone(UTC).strftime(W3CDTF_FORMAT)

    @classmethod
    def from_datetime_python(cls, dt: datetime) -> Self:
        """Wrap a plain ``datetime`` in ``cls`` without lexical parsing.

        Unlike :meth:`from_datetime`, this takes an existing ``datetime``
        instance (naive or aware) and copies its components. The value is
        range-checked against ``MIN_DATETIME..MAX_DATETIME``.

        Args:
            dt: A ``datetime`` instance. Naive values are kept naive
                (``tzinfo=None``); aware values keep their timezone.

        Returns:
            A new ``cls`` instance with the same components as ``dt``.

        Raises:
            TypeError: If ``dt`` is not a ``datetime`` instance.
            ValueError: If the instant lies outside
                ``MIN_DATETIME..MAX_DATETIME``
                (``1601-01-01T00:00:00Z`` .. ``9999-12-31T23:59:59.999999Z``).
        """
        if not isinstance(dt, datetime):
            raise TypeError(
                f"Expected datetime, got {type(dt).__name__}: {dt!r}"
            )
        cls._check_range(dt)
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo=dt.tzinfo,
            fold=dt.fold,
        )

    @classmethod
    def from_gyear(cls, s: str) -> Self:
        """Parse an ``xs:gYear`` lexical value.

        Args:
            s: A string like ``"2003"``, ``"2003Z"``, or ``"2003+09:00"``.

        Returns:
            A new instance with year set and month/day defaulted to 1.

        Raises:
            ValueError: If ``s`` is not a valid ``xs:gYear`` or the year is
                outside ``MIN_YEAR..MAX_YEAR`` (``1601..9999``).
        """
        m = GYEAR_RE.match(s)
        if not m:
            raise ValueError(f"Invalid xs:gYear: {s!r}")
        y = cls._parse_year(m.group("y"))
        return cls._apply_tz(cls(y, 1, 1), m.group("tz"))

    @classmethod
    def from_gyearmonth(cls, s: str) -> Self:
        """Parse an ``xs:gYearMonth`` lexical value.

        Args:
            s: A string like ``"2003-12"``, ``"2003-12Z"``, or
                ``"2003-12+09:00"``.

        Returns:
            A new instance with year and month set and day defaulted to 1.

        Raises:
            ValueError: If ``s`` is not a valid ``xs:gYearMonth`` or the
                year is outside ``MIN_YEAR..MAX_YEAR`` (``1601..9999``).
        """
        m = GYEARMONTH_RE.match(s)
        if not m:
            raise ValueError(f"Invalid xs:gYearMonth: {s!r}")
        y = cls._parse_year(m.group("y"))
        mo = int(m.group("mo"))
        return cls._apply_tz(cls(y, mo, 1), m.group("tz"))

    @classmethod
    def from_date(cls, s: str) -> Self:
        """Parse an ``xs:date`` lexical value.

        Args:
            s: A string like ``"2003-12-31"``, ``"2003-12-31Z"``, or
                ``"2003-12-31+09:00"``.

        Returns:
            A new instance with year, month, and day set.

        Raises:
            ValueError: If ``s`` is syntactically invalid, the year is
                outside ``MIN_YEAR..MAX_YEAR`` (``1601..9999``), or the
                date does not exist (e.g. ``2003-02-29``).
        """
        m = DATE_RE.match(s)
        if not m:
            raise ValueError(f"Invalid xs:date: {s!r}")
        y = cls._parse_year(m.group("y"))
        mo, d = int(m.group("mo")), int(m.group("d"))
        try:
            dt = cls(y, mo, d)
        except ValueError as e:
            raise ValueError(
                f"Invalid xs:date semantics: {s!r}: {e}"
            ) from None
        return cls._apply_tz(dt, m.group("tz"))

    @classmethod
    def from_datetime(cls, s: str) -> Self:
        """Parse an ``xs:dateTime`` lexical value.

        The input must be a W3CDTF ``dateTime``: ``YYYY-MM-DDThh:mm:ss``
        with an optional fractional second part (1..6 digits) and a
        mandatory timezone (``Z`` or ``±HH:MM``).

        Args:
            s: A string like ``"2003-12-31T10:14:55Z"`` or
                ``"2003-12-31T10:14:55.123-08:00"``.

        Returns:
            A new timezone-aware instance.

        Raises:
            ValueError: If ``s`` is not a valid W3CDTF ``dateTime`` or the
                resulting instant lies outside ``MIN_DATETIME..MAX_DATETIME``
                (``1601-01-01T00:00:00Z`` .. ``9999-12-31T23:59:59.999999Z``).
        """
        m = DATETIME_RE.match(s)
        if not m:
            raise ValueError(f"Invalid xs:dateTime: {s!r}")
        try:
            dt = datetime.fromisoformat(s)
        except ValueError as e:
            raise ValueError(
                f"Invalid xs:dateTime semantics: {s!r}: {e}"
            ) from None
        cls._check_range(dt)
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo=dt.tzinfo,
            fold=dt.fold,
        )

    @staticmethod
    def _parse_year(core: str) -> int:
        """Convert a lexical year (optionally prefixed with ``+``) to ``int``.

        Args:
            core: The year substring, e.g. ``"2003"`` or ``"+2003"``.

        Returns:
            The parsed year.

        Raises:
            ValueError: If the year is outside ``MIN_YEAR..MAX_YEAR``
                (``1601..9999``).
        """
        y = int(core)
        if not (MIN_YEAR <= y <= MAX_YEAR):
            raise ValueError(
                f"Year {y} is outside the supported range "
                f"{MIN_YEAR}..{MAX_YEAR}"
            )
        return y

    @staticmethod
    def _check_range(dt: datetime) -> None:
        """Validate that ``dt`` lies within the supported range.

        Aware values are compared in UTC; naive values are compared
        against naive copies of the bounds, so both kinds are accepted.

        Args:
            dt: The value to check.

        Raises:
            ValueError: If ``dt`` is outside ``MIN_DATETIME..MAX_DATETIME``.
        """
        if dt.tzinfo is None:
            lo = MIN_DATETIME.replace(tzinfo=None)
            hi = MAX_DATETIME.replace(tzinfo=None)
        else:
            lo, hi = MIN_DATETIME, MAX_DATETIME
            dt = dt.astimezone(UTC)
        if not (lo <= dt <= hi):
            raise ValueError(
                f"datetime {dt!r} is outside the supported range "
                f"{MIN_YEAR}..{MAX_YEAR}"
            )

    @classmethod
    def _apply_tz(cls, dt: datetime, tz_str: str | None) -> Self:
        """Attach a timezone to a naive ``datetime`` and wrap it in ``cls``.

        Args:
            dt: The source value; its date/time components are copied as-is.
            tz_str: ``None``, ``"Z"``, or an offset like ``"+09:00"`` /
                ``"-05:30"``.

        Returns:
            A new ``cls`` instance with the given timezone (or naive if
            ``tz_str`` is ``None``).
        """
        if tz_str is None:
            tz = None
        elif tz_str == "Z":
            tz = UTC
        else:
            sign = 1 if tz_str[0] == "+" else -1
            hh, mm = int(tz_str[1:3]), int(tz_str[4:6])
            tz = timezone(timedelta(hours=sign * hh, minutes=sign * mm))
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            tzinfo=tz,
            fold=dt.fold,
        )

    def _format_tz(self) -> str:
        """Format the instance's timezone as an XSD suffix.

        Returns:
            ``""`` if naive, ``"Z"`` for UTC, otherwise ``"+HH:MM"`` or
            ``"-HH:MM"``.
        """
        if self.tzinfo is None:
            return ""
        off = self.utcoffset()
        if off is None or off == timedelta(0):
            return "Z"
        total = int(off.total_seconds() // 60)
        sign = "+" if total >= 0 else "-"
        total = abs(total)
        return f"{sign}{total//60:02d}:{total%60:02d}"
