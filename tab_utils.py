from dataclasses import dataclass


@dataclass
class Tab:
    name: str
    string_count: float
    tuning: list
    frames: list

    def save(self):
        pass
