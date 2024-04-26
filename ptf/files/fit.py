import datetime
from pathlib import Path

import fitdecode

from ptf.data import Duration, Pace, Range


class FitFileLoader:
    def load(self, fit_path: Path):
        data = {"hr": Range(None, None, None)}
        with fitdecode.FitReader(fit_path) as fit:
            for frame in fit:

                # Get session data
                if (
                    frame.frame_type == fitdecode.FIT_FRAME_DATA
                    and frame.name == "session"
                ):
                    for field in frame.fields:
                        if field.name == "total_timer_time":
                            data["duration"] = Duration(seconds=field.value)
                        elif field.name == "total_elapsed_time":
                            data["elapsed"] = Duration(seconds=field.value)
                        elif field.name == "total_distance":
                            data["distance"] = field.value / 1000.0
                        elif field.name == "avg_heart_rate":
                            data["hr"].avg_value = field.value
                        elif field.name == "max_heart_rate":
                            data["hr"].max_value = field.value
                        elif field.name == "avg_running_cadence":
                            data["cadence"] = field.value
        data["pace"] = Pace(seconds=data["duration"].total_seconds() / data["distance"])
        return data, {}
