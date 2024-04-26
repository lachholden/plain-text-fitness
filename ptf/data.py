import datetime
from dataclasses import dataclass, field
from math import floor
from pathlib import Path
from typing import Any, Dict, Generic, Optional, TypeVar


class Pace(datetime.timedelta):
    """Represents a pace per some unit distance (i.e. typically time per km.)"""

    def __repr__(self):
        secs = floor(self.total_seconds())
        micros = self.total_seconds() - secs
        mm = floor(secs / 60)
        secs -= mm * 60
        ss = floor(secs)
        string = f"{mm}'{ss:02d}"
        string += f"{micros}".lstrip("0") + '"'
        return string


class Duration(datetime.timedelta):
    def __repr__(self):
        secs = floor(self.total_seconds())
        micros = self.total_seconds() - secs
        hh = floor(secs / 60 / 60)
        secs -= hh * 60 * 60
        mm = floor(secs / 60)
        secs -= mm * 60
        ss = floor(secs)
        if hh > 0:
            string = f"{hh}:{mm:02d}:{ss:02d}"
        else:
            string = f"{mm}:{ss:02d}"
        string += f"{micros}".lstrip("0")
        return string


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
