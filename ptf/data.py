import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Activity:
    date: datetime.date
    activity_type: str
    tags: Optional[set[str]] = field(default_factory=set)
    data: Dict[str, Any] = field(default_factory=dict)
