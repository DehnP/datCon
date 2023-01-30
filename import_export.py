import tkinter
from tkinter import filedialog
import numpy as np
from array_logic import *
import pickle
from txt_logic import *
from classes import *


def open_file_location_event(file_loc_entry) -> None:
    # open file location
    print("open_file_location_event")
    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window
    tempdir = filedialog.askopenfilename(parent=root, title='Please select a file', filetypes=[
        ('Text file', '.txt'), ('.dat file', '.dat')])
    # Insert file path into entry box
    if len(tempdir) > 0:
        file_loc_entry.delete(0, 'end')
        file_loc_entry.insert(0, tempdir)


def save_profile_event(file_loc_entry, file_name_entry) -> None:
    # save profile to /Profiles
    if len(file_name_entry.get()) == 0:
        print("No File Name")
        return
    else:
        array = strip_dat_to_array(file_loc_entry.get())
        savePath = ("Profiles/"+file_name_entry.get()+".txt")
        np.savetxt(savePath, array, fmt='%1.6f', delimiter=",")


def load_blade_event(current_blade: Blade) -> Blade:
    # load blade from file
    print("load_blade_event")
    root = tkinter.Tk()
    root.withdraw()
    tempdir = filedialog.askopenfilename(
        parent=root, title='Please select a file', filetypes=[('Text file', '.txt')])
    if len(tempdir) > 0:
        with open(tempdir, 'rb') as f:
            current_blade = pickle.load(f)
    print(current_blade.sections[0].coords)
    return current_blade


def open_save_location_event(save_loc_entry) -> None:
    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window
    tempdir = filedialog.askdirectory(
        parent=root, title='Please select a folder')
    if len(tempdir) > 0:
        save_loc_entry.delete(0, 'end')
        save_loc_entry.insert(0, tempdir)


def export_curves_event(current_blade, save_loc_entry, file_name_entry) -> None:
    # Export curves to SC compatible format
    print("export_curves_event")

    # create temp array
    temp_array = np.array(current_blade.sections[0].coords)
    temp_full_array = temp_array

    # read rest of sections and add to tempFullArray
    for i in range(1, len(current_blade.sections)):
        temp_array = np.array(current_blade.sections[i].coords)
        # append to tempFullArray
        temp_full_array = np.concatenate((temp_full_array, temp_array), axis=0)
    print(temp_full_array)
    # round values in tempFullArray to 8 decimal places
    temp_full_array = np.around(temp_full_array, decimals=8)

    # save to file
    np.savetxt(save_loc_entry.get() + "\\" + file_name_entry.get() +
               ".txt", temp_full_array, delimiter=",", fmt='%.6f')
    add_blank_line(save_loc_entry.get() + "\\" +
                   file_name_entry.get() + ".txt")
    prepend_line_to_file(save_loc_entry.get(
    ) + "\\" + file_name_entry.get() + ".txt", "3d=true")


def save_blade_event(blade_name_entry, current_blade):
    # save blade to file
    print("save_blade_event")
    # get blade name from entry box
    blade_Name = blade_name_entry.get()
    with open('Blades/' + blade_Name + '.txt', 'wb') as f:
        pickle.dump(current_blade, f)
