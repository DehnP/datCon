from dataclasses import dataclass
import numpy as np
from typing import Dict, Optional


class Blade:
    def __init__(self, sections: Dict[int, 'Section'] = {}):
        """
        Initialize a Blade object with a dictionary of sections, where the key is the section number (n) and the value is the Section object.

        :param sections: Dictionary of sections (default: empty dictionary)
        :type sections: Dict[int, Section]
        """
        self.sections = sections

    def add_section(self, section: 'Section'):
        """
        Add a new section to the sections dictionary, using the section number (n) as the key.

        :param section: Section to add
        :type section: Section
        """
        self.sections[section.n] = section

    def remove_section(self, n: int):
        """
        Remove the section with the specified section number (n) from the sections dictionary.

        :param n: Section number of the section to remove
        :type n: int
        """
        del self.sections[n]

    def get_section(self, n: int) -> Optional['Section']:
        """
        Retrieve the section with the specified section number (n).

        :param n: Section number of the section to retrieve
        :type n: int
        :return: Section with the specified section number, or None if not found
        :rtype: Optional[Section]
        """
        return self.sections.get(n)

    def clear_sections(self):
        """
        Remove all sections from the sections dictionary.
        """
        self.sections.clear()


@dataclass
class Section:
    n: int  # section number
    dr: float  # displacement
    twist: float  # twist angle
    chord: float  # chord length
    profile: np.array  # profile coordinates
    coords: np.array  # 3D coordinates
