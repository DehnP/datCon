import numpy as np
import os

# Function to read in the data from the .txt files
def strip_txt_to_array(file_path):
    array = []
    with open(file_path) as text_file:
        lines = text_file.readlines()
    del lines[0]
    for line in lines:
        array1 = [item.strip() for item in line.split()]
        array.append(array1)
    array = np.asarray(array, dtype=np.float16)    
    return array

# Function to add a column of ones to the data (spaceclaim)
def add_ones(array):
    array = np.asarray(array, dtype=np.float16)
    ones = np.ones((array.shape[0], 3))
    ones[:, 1:3] = array
    return ones

# Function to multiply the data by the chord length
def multiply_by_chord_length(chord_length, array):
    array[:, 1:3] *= chord_length
    return array

# Function to write the data to a .txt file
def prepend_line_to_file(file_path, line):
    dummy_file = file_path + '.bak'
    with open(file_path, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        write_obj.write(line + '\n')
        for line in read_obj:
            write_obj.write(line)
    os.remove(file_path)
    os.rename(dummy_file, file_path)

#========JANK CODE TO REMOVE .000000 FROM END OF EACH LINE========

def remove_decimal_zeros(savePath):
# Specify the string to be deleted and the file path
    string_to_delete = ".000000"

    # Open the file in read mode and read the contents into a string
    with open(savePath, "r") as f:
        contents = f.read()

    # Replace all instances of the string with an empty string
    modified_contents = contents.replace(string_to_delete, "")

    # Open the file in write mode and write the modified string to the file
    with open(savePath, "w") as f:
        f.write(modified_contents)

    # Close the file
    f.close()