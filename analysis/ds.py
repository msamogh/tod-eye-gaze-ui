from typing import Text, List, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GazePath:
    submit_time: datetime
    dst: Dict[Text, Text]
    turns_time_series: Dict[int, int]
    prompt: str

    def __post_init__(self):
        if self.prompt not in ["goal", "semi"]:
            raise ValueError(f"Invalid prompt: {self.prompt}")


@dataclass
class Participant:
    name: str
    email: str
    start_time: datetime
    calibaration_quality: int
    gaze_paths: List[GazePath] = field(default_factory=list)
