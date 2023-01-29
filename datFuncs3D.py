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

