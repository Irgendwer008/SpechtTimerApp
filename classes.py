from dataclasses import dataclass
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
        self.current_checkpoint = -1
        self.laps = []

    def start(self):
        self.start_time = time.perf_counter()
        self.date = datetime.now()

    def next_checkpoint(self) -> str:

        t = time.perf_counter()

        if (len(self.laps) == 0) or (self.current_checkpoint + 1 >= len(self.checkpoints)):
            self.laps.append(Lap(len(self.laps), t, []))
        
        current_lap = self.laps[-1]

        current_lap.relative_checkpoint_times.append(t - current_lap.start_time)
        self.current_checkpoint = (self.current_checkpoint + 1) % len(self.checkpoints)

        description = self.checkpoints[self.current_checkpoint]
        
        time1 = t - current_lap.start_time
        # if first lap
        if current_lap.number == 0:
            time2 = None
        else:
            # if start/finish
            if self.current_checkpoint == 0:
                time1 = current_lap.start_time - self.laps[-2].start_time
                if current_lap.number == 1:
                    time2 = None
                else:
                    time2 = time1 - (self.laps[-2].start_time - self.laps[-3].start_time)

            else:
                time2 = time1 - self.laps[-2].relative_checkpoint_times[self.current_checkpoint]
        
        return f"{description}: {format_time(time1)} ({format_time(time2, timediff = True)})"
    
    def redo_checkpoint(self) -> str:
        pass

    def get_lap_count(self) -> int:
        return len(self.laps)
    
    def elapsed(self) -> float:
        return time.perf_counter() - self.start_time

    def to_xml(self) -> str:
        return ""

@dataclass
class Lap:
    number: int
    start_time: float
    relative_checkpoint_times: list[int]