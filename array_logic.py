import numpy as np
import os
import pandas as pd


def strip_dat_to_array(file_path) -> np.array:
    array = []
    with open(file_path) as text_file:
        lines = text_file.readlines()
    del lines[0]  # remove header
    for line in lines:
        array1 = [item.strip() for item in line.split()]
        array.append(array1)
    array = np.asarray(array, dtype=np.float16)
    return array


def strip_profile_to_array(file_path) -> np.array:
    array = np.loadtxt(file_path, delimiter=',', dtype=np.float16)
    return array


def scale_profile(profile, scale_factor: float) -> np.array:
    profile = profile * scale_factor
    return profile


def rotate_profile(profile, angle: float) -> np.array:
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    profile = np.dot(R, profile.T).T
    return profile


def add_displacement_column(array, n, dr) -> np.array:
    radial_dist = dr * n
    array = np.insert(array, 0, radial_dist, axis=1)
    return array
