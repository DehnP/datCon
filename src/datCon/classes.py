from dataclasses import dataclass
import numpy as np


class Blade:
    def __init__(self, sections=[]):
        self.sections = sections  # list of sections

    def add_section(self, section):
        # check if a section with the same n value exists
        for i, s in enumerate(self.sections):
            if s.n == section.n:
                self.sections.pop(i)  # remove existing section
                break
        self.sections.append(section)  # add new section to list of sections


@dataclass
class Section:
    n: int  # section number
    dr: float  # displacement
    twist: float  # twist angle
    chord: float  # chord length
    profile: np.array  # profile coordinates
    coords: np.array  # 3D coordinates
