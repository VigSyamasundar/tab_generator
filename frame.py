from dataclasses import dataclass


@dataclass
class Frame:
    notes: dict

    def initialise(self, tuning):
        self.notes = {}
        for string in tuning:
            self.notes[string] = ""
