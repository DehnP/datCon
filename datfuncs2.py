import numpy as np
import os

#==========Strip txt to array & Remove first line=========#
def OpenTextFile(datPath):
    array = []

    with open (datPath) as textFile:
        lines = textFile.readlines()
    del lines[0]
    new_file = open(datPath,"w+")
    for line in lines:
        new_file.write(line)
    new_file.close()

    with open (datPath) as textFile:
        for line in textFile:
            array1 = [item.strip() for item in line.split()]
            array.append(array1)            
    return array

#==========Add ones to array=========#
def AddOnes(array):
    PP = np.asarray(array, dtype=np.float16)
    z = np.ones((PP.shape[0],3))
    z[:, 1:3] = PP
    return z

#==========Multiply by chord length=========#
def chordMult(CL,arr):
    arr[:,1:3] *= CL
    return arr

#==========Add Polyline=true===============#
def prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
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