import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from math import floor
from pathlib import Path
from re import I
from typing import Any, Dict, Generic, Optional, TypeVar

MINS = "\u2032"
SECS = "\u2033"


class Pace:
    """Represents a pace per some unit distance (i.e. typically time per km.)

    Minimum resolution is seconds, and can support arbitrary fractional-second
    resolution.

    Stored as a Decimal quantity of seconds in self.seconds.
    """

    def __init__(self, seconds: Decimal):
        self.seconds = Decimal(seconds)

    def __str__(self):
        mm = self.seconds // 60
        ss = self.seconds - mm * 60
        return f"{mm}{MINS}{ss:02f}{SECS}"

    def __repr__(self):
        return f"Pace({str(self)})"


class Duration:
    """Represents a duration of time.

    Supports resolutions of minutes, seconds, and arbitrary fractional-second
    resolutions.

    For minute resolution, the number of minutes is stored as an int in self.minutes,
    and self.seconds is None. (TODO currently unimplemented)

    For second or sub-second resolution, the number of minutes is stored as an int in
    self.minutes, and then *remaining* seconds and fractions thereof are stored as a
    Decimal in self.seconds. Hence, 0 <= self.seconds < 60
    """

    def __init__(self, seconds: Decimal):
        self.seconds = Decimal(seconds)
        decimal_minutes = self.seconds // 60
        self.seconds -= decimal_minutes * 60
        self.minutes = int(decimal_minutes)

    def total_seconds(self) -> Decimal:
        return self.seconds + self.minutes * 60

    def __str__(self):
        hh = self.minutes // 60
        mm = self.minutes - hh * 60
        ss = self.seconds

        if hh > 0:
            return f"{hh}:{mm:02d}:{ss:02f}"
        else:
            return f"{mm}:{ss:02f}"

    def __repr__(self):
        return f"Duration({str(self)})"


@dataclass
class Activity:
    date: datetime.date
    activity_type: str
    tags: Optional[set[str]] = field(default_factory=set)
    data: Dict[str, Any] = field(default_factory=dict)

    def related_file_paths(self, root_directory: Path) -> list[Path]:
        activity_dir = root_directory.joinpath(*self.activity_type.split(":"))
        return [
            f
            for f in activity_dir.iterdir()
            if f.name.startswith(self.date.isoformat())
        ]


T = TypeVar("T")


@dataclass
class Range(Generic[T]):
    min_value: Optional[T] = None
    avg_value: Optional[T] = None
    max_value: Optional[T] = None

    def __repr__(self):
        string = ""
        if self.min_value:
            string += f"{repr(self.min_value)} < "
        if self.avg_value:
            string += repr(self.avg_value)
        if self.max_value:
            string += f" > {repr(self.max_value)}"
        return string
