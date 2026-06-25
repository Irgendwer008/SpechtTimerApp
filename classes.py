from dataclasses import dataclass, field
from datetime import datetime
from helper import format_time
import time

class Session:
    date: datetime
    start_time: float
    checkpoints: tuple[str]
    current_checkpoint: int
    laps: list[Lap]

    def __init__(self, checkpoints: tuple[str]):
        self.date = None
        self.start_time = None
        self.checkpoints = checkpoints
        self.current_checkpoint = 0
        self.laps = []

    def start(self):
        self.start_time = time.perf_counter()
        self.date = datetime.now()
        self.laps.append(Lap(time.perf_counter()))

    def next_checkpoint(self) -> str:
        newlap = False
        t = time.perf_counter()

        current_lap = self.laps[-1]

        # The checkpoint we're recording right now
        checkpoint_idx = self.current_checkpoint

        time1 = t - current_lap.start_time
        current_lap.relative_checkpoint_times.append(time1)

        if current_lap.number == 0:
            time2 = None
        else:
            prev_lap = self.laps[-2]

            if checkpoint_idx < len(prev_lap.relative_checkpoint_times):
                time2 = (
                    time1
                    - prev_lap.relative_checkpoint_times[checkpoint_idx]
                )
            else:
                time2 = None

        summary = f"{format_time(time1)} ({format_time(time2, time_diff = True)})"

        # Advance to the next checkpoint
        if checkpoint_idx + 1 >= len(self.checkpoints):
            self.laps.append(Lap(t, number=len(self.laps)))
            self.current_checkpoint = 0
        else:
            self.current_checkpoint = checkpoint_idx + 1
        
        return summary, time2
    
    def redo_checkpoint(self) -> str:
        if len(self.laps[-1].relative_checkpoint_times) == 0:
            self.laps.pop()

        self.laps[-1].relative_checkpoint_times.pop()

        if self.current_checkpoint > 0:
            self.current_checkpoint -= 1
        else:
            self.current_checkpoint = len(self.checkpoints) - 1

        return self.next_checkpoint()

    def get_lap_count(self) -> int:
        return len(self.laps)
    
    def elapsed(self) -> float:
        return time.perf_counter() - self.start_time

    def to_xml(self) -> str:
        return ""

@dataclass
class Lap:
    start_time: float
    number: int = 0
    relative_checkpoint_times: list[int] = field(default_factory=list)