import numpy as np


def strip_dat_to_array(file_path) -> np.array:
    return np.genfromtxt(file_path, skip_header=1, dtype=np.float16)


def strip_profile_to_array(file_path) -> np.array:
    array = np.loadtxt(file_path, delimiter=',', dtype=np.float16)
    return array


def calculate_section_coords(profile, scale_factor: float, angle: float, dr: float, n: int) -> np.array:
    profile = profile * scale_factor

    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    profile = np.dot(profile, R.T)

    radial_dist = dr * n
    profile = np.insert(profile, 0, radial_dist, axis=1)

    return profile
