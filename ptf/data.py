import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Generic, Optional, TypeVar


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
