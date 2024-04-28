import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import fitdecode

from ptf.data import Duration, Pace, Range


class FitFileLoader:
    def load(self, fit_path: Path):
        data: dict[str, Any] = {"hr": Range(None, None, None)}
        with fitdecode.FitReader(fit_path) as fit:
            for frame in fit:

                # Get session data
                if (
                    frame.frame_type == fitdecode.FIT_FRAME_DATA
                    and frame.name == "session"
                ):
                    for field in frame.fields:
                        if field.name == "total_timer_time":
                            data["duration"] = Duration(
                                seconds=round(
                                    Decimal(field.raw_value) / Decimal("1e3"), 0
                                )
                            )
                        elif field.name == "total_elapsed_time":
                            data["elapsed"] = Duration(
                                seconds=round(
                                    Decimal(field.raw_value) / Decimal("1e3"), 0
                                )
                            )
                        elif field.name == "total_distance":
                            data["distance"] = round(
                                Decimal(field.raw_value) / Decimal("1e5"), 2
                            )
                        elif field.name == "avg_heart_rate":
                            data["hr"].avg_value = Decimal(field.value)
                        elif field.name == "max_heart_rate":
                            data["hr"].max_value = Decimal(field.value)
                        elif field.name == "avg_running_cadence":
                            data["cadence"] = Decimal(field.value)
        data["pace"] = Pace(
            seconds=(data["duration"].total_seconds() / data["distance"]).quantize(
                Decimal("1")
            )
        )
        return data, {}
