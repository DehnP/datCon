import numpy as np
import os

def read_array_from_file(file_path):
    """
    Read a list of numbers from a text file, skip the first line, and return
    the numbers as a 2D NumPy array.
    """
    array = []

    with open(file_path) as file:
        lines = file.readlines()
    # skip the first line
    lines = lines[1:]
    # write the remaining lines back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

    # read the numbers from the file
    with open(file_path) as file:
        for line in file:
            array1 = [float(item) for item in line.split()]
            array.append(array1)
    return np.array(array)

def add_ones_column(array):
    """
    Add a column of ones to the left of a 2D NumPy array.
    """
    z = np.ones((array.shape[0], 3))
    z[:, 1:3] = array
    return z

def multiply_by_chord_length(chord_length, array):
    """
    Multiply the second and third columns of a 2D NumPy array by a given
    chord length.
    """
    array[:, 1:3] *= chord_length
    return array

def prepend_line_to_file(file_name, line):
    """
    Insert a given string as a new line at the beginning of a file.
    """
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)