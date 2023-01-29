import numpy as np
import os
import pandas as pd

# Function to read in the data from dat .txt files
def strip_dat_to_array(file_path):
    array = []
    with open(file_path) as text_file:
        lines = text_file.readlines()
    del lines[0] # remove header
    for line in lines:
        array1 = [item.strip() for item in line.split()]
        array.append(array1)
    array = np.asarray(array, dtype=np.float16)    
    return array

# Function to strip profile coordinates to a numpy array from a .txt file
def strip_profile_to_array(file_path):
    array = np.loadtxt(file_path,delimiter=',', dtype=np.float16)
    return array

# Function to scale a profile coordinates by a scale factor
def scale_profile(profile, scale_factor: float):
    profile = profile * scale_factor
    return profile

# function to rotate a profile by a given angle about 0,0
def rotate_profile(profile, angle: float):
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c,-s), (s, c)))
    profile = np.dot(R, profile.T).T
    return profile


# Function which adds a column (displacement x section index) to the left of the array
def add_displacement_column(array,n,dr):
    radialDist = dr * n
    array = np.insert(array, 0, radialDist, axis=1)
    return array

# Function to add a blank line after every 35th line in a .txt file
def add_blank_line(file_path):
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        line_count = 1
        for line in lines:
            file.write(line)
            if line_count % 35 == 0:
                file.write("\n")
            line_count += 1

def prepend_line_to_file(file_path, line):
    dummy_file = file_path + '.bak'
    with open(file_path, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        write_obj.write(line + '\n')
        for line in read_obj:
            write_obj.write(line)
    os.remove(file_path)
    os.rename(dummy_file, file_path)
