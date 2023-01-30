import tkinter
from tkinter import filedialog
from matplotlib.figure import Figure
import customtkinter as ctk
import numpy as np
from datFuncs3D import *
from PIL import Image
import os
from dataclasses import dataclass
import pickle
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set appearance mode and default color theme
        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("System")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("blue")
        self.resizable(0, 0)
        # self.geometry("1000x600")
        self.title("datConv")
        self.iconbitmap("Assets/datCon.ico")
        # initialize the window
        self.main_view()
        self.current_blade = Blade()

    def main_view(self):
        titles_font = ctk.CTkFont(family="Arciform", size=20)
        text_font = ctk.CTkFont(family="Arciform", size=12)
        # =====================FRAMING==================================================
        self.master_frame = ctk.CTkFrame(self)
        self.master_frame.pack(pady=5, padx=5, fill='both', expand=True)

        self.right_frame = ctk.CTkFrame(self.master_frame)
        self.right_frame.pack(side='right', fill='both',
                              expand=True, padx=5, pady=5)
        # ===============================================================================

        # =====================leftFrame==================================================
        self.tab_view = ctk.CTkTabview(self.master_frame)
        self.tab_view.pack(fill='both', expand=True,
                           padx=5, pady=5, side='left')
        self.config_tab = self.tab_view.add("Config")
        self.import_tab = self.tab_view.add("Import/Export")

        # =====================Config==================================================
        self.config_frame = ctk.CTkFrame(self.config_tab)
        self.config_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Config Widgets
        self.profile_frame = ctk.CTkFrame(self.config_frame)
        self.profile_frame.pack(fill='x', expand=True,
                                padx=5, pady=5, anchor='n')

        # section quantity
        self.num_of_profiles_INT = 1
        self.section_quantity_label = ctk.CTkLabel(
            self.profile_frame, text="Number of sections: ", font=text_font)
        self.section_quantity_label.pack(side='left', padx=5, pady=5)
        self.section_quantity_entry = ctk.CTkEntry(
            self.profile_frame, font=text_font, width=55)
        self.section_quantity_entry.pack(side='left', padx=5, pady=5)
        self.section_quantity_entry.insert(0, "1")

        # profile displacement
        self.profile_disp_label = ctk.CTkLabel(
            self.profile_frame, text="Displacement", font=text_font)
        self.profile_disp_label.pack(side='left', padx=5, pady=5)
        self.profile_disp_entry = ctk.CTkEntry(
            self.profile_frame, font=text_font, width=55)
        self.profile_disp_entry.pack(side='left', padx=5, pady=5)
        self.profile_disp_entry.insert(0, "0")

        # set button
        self.set_button = ctk.CTkButton(
            self.profile_frame, text="Set", font=text_font, command=self.change_number_of_profile_event)
        self.set_button.pack(side='right', padx=5, pady=5)

        # profile config frame
        self.profile_config_frame = ctk.CTkFrame(self.config_frame)
        self.profile_config_frame.pack(
            fill='x', expand=True, padx=5, pady=5, anchor='n')

        # section select
        self.section_select_label = ctk.CTkLabel(
            self.profile_config_frame, text="Section: ", font=text_font)
        self.section_select_label.pack(side='left', padx=5, pady=5)
        self.section_select_option = ctk.CTkOptionMenu(self.profile_config_frame, values=[
            "1"], font=text_font, width=55)
        self.section_select_option.pack(side='left', padx=5, pady=5)
        self.section_select_option.set(1)

        # profile Twist
        self.section_twist_label = ctk.CTkLabel(
            self.profile_config_frame, text="Twist: ", font=text_font)
        self.section_twist_label.pack(side='left', padx=5, pady=5)
        self.section_twist_entry = ctk.CTkEntry(
            self.profile_config_frame, font=text_font, width=55)
        self.section_twist_entry.pack(side='left', padx=5, pady=5)
        self.section_twist_entry.insert(0, "0")

        # profile Chord
        self.section_chord_label = ctk.CTkLabel(
            self.profile_config_frame, text="Chord: ", font=text_font)
        self.section_chord_label.pack(side='left', padx=5, pady=5)
        self.section_chord_entry = ctk.CTkEntry(
            self.profile_config_frame, font=text_font, width=55)
        self.section_chord_entry.pack(side='left', padx=5, pady=5)
        self.section_chord_entry.insert(0, "1")

        # profile select
        self.profile_select_label = ctk.CTkLabel(
            self.profile_config_frame, text="Profile: ", font=text_font)
        self.profile_select_label.pack(side='left', padx=5, pady=5)

        # list of profile txt files in the profile folder
        self.list_profiles()

        self.profile_select_option = ctk.CTkOptionMenu(
            self.profile_config_frame, values=self.profile_list, font=text_font, width=55)
        self.profile_select_option.pack(side='left', padx=5, pady=5)
        self.profile_select_option.set("")

        # profile save button
        self.profile_save_button = ctk.CTkButton(
            self.profile_config_frame, text="Save", font=text_font, command=self.save_section_config_event)
        self.profile_save_button.pack(side='right', padx=5, pady=5)

        # save Blade Frame
        self.save_blade_frame = ctk.CTkFrame(self.config_frame)
        self.save_blade_frame.pack(
            fill='x', expand=True, padx=5, pady=5, anchor='n')

        # save Blade Button
        self.save_blade_button = ctk.CTkButton(
            self.save_blade_frame, text="Save Blade", font=text_font, command=self.save_blade_event)
        self.save_blade_button.pack(side='right', padx=5, pady=5)

        # save Blade Name Entry
        self.save_blade_name_entry = ctk.CTkEntry(
            self.save_blade_frame, font=text_font, width=100)
        self.save_blade_name_entry.pack(side='right', padx=5, pady=5)
        self.save_blade_name_entry.insert(0, "Blade Name")

        # plot Blade Frame
        self.plot_blade_frame = ctk.CTkFrame(self.config_frame)
        self.plot_blade_frame.pack(
            fill='x', expand=True, padx=5, pady=5, anchor='n')
        # plot Blade Button
        self.plot_blade_button = ctk.CTkButton(
            self.plot_blade_frame, text="Plot Blade", font=text_font, command=self.plot_blade_event)
        self.plot_blade_button.pack(side='right', padx=5, pady=5)

        # load Blade Frame
        self.load_blade_frame = ctk.CTkFrame(self.config_frame)
        self.load_blade_frame.pack(
            fill='x', expand=True, padx=5, pady=5, anchor='n')
        # load Blade Button
        self.load_blade_button = ctk.CTkButton(
            self.load_blade_frame, text="Load Blade", font=text_font, command=self.load_blade_event)
        self.load_blade_button.pack(side='right', padx=5, pady=5)

        # =====================Save/Load==================================================
        self.save_load_frame = ctk.CTkFrame(self.import_tab)
        self.save_load_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Save/Load Widgets
        self.save_load_frame = ctk.CTkFrame(self.save_load_frame)
        self.save_load_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.folder_icon = ctk.CTkImage(
            light_image=Image.open("Assets/Folder.png"))
        self.file_loc_label = ctk.CTkLabel(
            self.save_load_frame, text='Import .dat File Location:')
        self.file_loc_label.grid(
            row=0, column=0, columnspan=3, sticky='nsew', pady=2)

        self.file_loc_entry = ctk.CTkEntry(
            self.save_load_frame, placeholder_text='C:\\..', width=300)
        self.file_loc_entry.grid(
            row=1, column=0, sticky='nsew', pady=2, columnspan=2)

        self.file_loc_open = ctk.CTkButton(
            self.save_load_frame, text='', width=20, image=self.folder_icon, command=self.open_file_location_event)
        self.file_loc_open.grid(row=1, column=2, sticky='nsew', pady=2)

        self.file_name_label = ctk.CTkLabel(
            self.save_load_frame, text='File Name')
        self.file_name_label.grid(row=2, column=0, sticky='nsew', pady=2)

        self.file_name_entry = ctk.CTkEntry(
            self.save_load_frame, placeholder_text='NACAXXXX..')
        self.file_name_entry.grid(row=3, column=0, sticky='nsew', pady=2)

        self.file_save = ctk.CTkButton(
            self.save_load_frame, text='Save', width=50, command=self.save_profile_event)
        self.file_save.grid(row=3, column=1, columnspan=3, sticky='nsew')

        self.save_loc_label = ctk.CTkLabel(
            self.save_load_frame, text='Export SC compatible Save Location:')
        self.save_loc_label.grid(
            row=4, column=0, columnspan=3, sticky='nsew', pady=2)

        self.save_loc_entry = ctk.CTkEntry(
            self.save_load_frame, placeholder_text='D:\\..', width=300)
        self.save_loc_entry.grid(
            row=5, column=0, sticky='nsew', pady=2, columnspan=2)

        self.save_loc_open = ctk.CTkButton(
            self.save_load_frame, text='', width=20, image=self.folder_icon, command=self.open_save_location_event)
        self.save_loc_open.grid(row=5, column=2, sticky='nsew', pady=2)

        self.file_name_label = ctk.CTkLabel(
            self.save_load_frame, text='File Name')
        self.file_name_label.grid(row=6, column=0, sticky='nsew', pady=2)

        self.file_name_entry = ctk.CTkEntry(
            self.save_load_frame, placeholder_text='NACAXXXX..')
        self.file_name_entry.grid(row=7, column=0, sticky='nsew', pady=2)

        self.file_save = ctk.CTkButton(
            self.save_load_frame, text='Save', width=50, command=self.export_curves_event)
        self.file_save.grid(row=7, column=1, columnspan=3, sticky='nsew')

        # =====================rightFrame==================================================
        self.plot_view_label = ctk.CTkLabel(
            self.right_frame, text="Plot View", font=titles_font)
        self.plot_view_label.pack(side='top', padx=5, pady=5)

        self.plot_view_frame = ctk.CTkFrame(self.right_frame)
        self.plot_view_frame.pack(fill='both', expand=True, padx=10, pady=10)

# =====================METHODS==================================================
    def open_save_location_event(self):
        root = tkinter.Tk()
        root.withdraw()  # use to hide tkinter window
        tempdir = filedialog.askdirectory(
            parent=root, title='Please select a folder')
        if len(tempdir) > 0:
            self.save_loc_entry.delete(0, 'end')
            self.save_loc_entry.insert(0, tempdir)

    def export_curves_event(self):
        # Export curves to SC compatible format
        print("export_curves_event")

        # create temp array
        tempArray = np.array(self.current_blade.sections[0].coords)
        tempFullArray = tempArray

        # read rest of sections and add to tempFullArray
        for i in range(1, len(self.current_blade.sections)):
            tempArray = np.array(self.current_blade.sections[i].coords)
            # append to tempFullArray
            tempFullArray = np.concatenate((tempFullArray, tempArray), axis=0)
        print(tempFullArray)
        # round values in tempFullArray to 8 decimal places
        tempFullArray = np.around(tempFullArray, decimals=8)

        # save to file
        np.savetxt(self.save_loc_entry.get() + "\\" + self.file_name_entry.get() +
                   ".txt", tempFullArray, delimiter=",", fmt='%.6f')
        add_blank_line(self.save_loc_entry.get() + "\\" +
                       self.file_name_entry.get() + ".txt")
        prepend_line_to_file(self.save_loc_entry.get(
        ) + "\\" + self.file_name_entry.get() + ".txt", "3d=true")

    def change_number_of_profile_event(self):
        print("change_number_of_profile_event")
        # get value from profile quantity entry
        self.num_of_profiles_INT = int(self.section_quantity_entry.get())
        options = [str(i) for i in range(1, self.num_of_profiles_INT+1)]
        # update the options in the profile select option menu
        self.section_select_option.configure(values=options)

    def save_section_config_event(self):
        # Save configuration of section
        print("save_profile_event")
        # get values from entry boxes
        section_index = int(self.section_select_option.get())
        section_displacement = float(self.profile_disp_entry.get())
        section_twist = float(self.section_twist_entry.get())
        section_chord = float(self.section_chord_entry.get())
        # strip the .txt from the profile name
        temp_profile_name = self.profile_select_option.get()
        section_profile = strip_profile_to_array(
            "Profiles/" + temp_profile_name + ".txt")

        # generate coords for profile
        section_coords = scale_profile(section_profile, section_chord)
        section_coords = rotate_profile(section_coords, section_twist)
        section_coords = add_displacement_column(
            section_coords, section_index, section_displacement)

        # save to class 'section' object
        temp_section = Section(section_index, section_displacement,
                               section_twist, section_chord, section_profile, section_coords)

        # save to class 'blade' object
        self.current_blade.add_section(temp_section)

        print(temp_section)
        print(self.current_blade.sections)

    def save_blade_event(self):
        # save blade to file
        print("save_blade_event")
        # get blade name from entry box
        bladeName = self.save_blade_name_entry.get()
        with open('Blades/' + bladeName + '.txt', 'wb') as f:
            pickle.dump(self.current_blade, f)

    def load_blade_event(self):
        # load blade from file
        print("load_blade_event")
        root = tkinter.Tk()
        root.withdraw()
        tempdir = filedialog.askopenfilename(
            parent=root, title='Please select a file', filetypes=[('Text file', '.txt')])
        if len(tempdir) > 0:
            with open(tempdir, 'rb') as f:
                self.current_blade = pickle.load(f)

    def load_profile_event(self):
        # load dat file
        print("load_profile_event")

    def open_file_location_event(self):
        # open file location
        print("open_file_location_event")
        root = tkinter.Tk()
        root.withdraw()  # use to hide tkinter window
        tempdir = filedialog.askopenfilename(parent=root, title='Please select a file', filetypes=[
                                             ('Text file', '.txt'), ('.dat file', '.dat')])
        # Insert file path into entry box
        if len(tempdir) > 0:
            self.file_loc_entry.delete(0, 'end')
            self.file_loc_entry.insert(0, tempdir)

    def save_profile_event(self):
        # save profile to /Profiles
        if len(self.file_name_entry.get()) == 0:
            print("No File Name")
            return
        else:
            array = strip_dat_to_array(self.file_loc_entry.get())
            savePath = ("Profiles/"+self.file_name_entry.get()+".txt")
            np.savetxt(savePath, array, fmt='%1.6f', delimiter=",")

    def list_profiles(self):
        # list all profiles in the profile folder
        self.profile_list = []
        for file in os.listdir("Profiles"):
            if file.endswith(".txt"):
                self.profile_list.append(file.replace(".txt", ""))

    def plot_blade_event(self):
        # plot blade
        print("plot_blade_event")
        # concatenate all sections
        blade_coords = np.array([])
        for section in self.current_blade.sections:
            if blade_coords.size == 0:
                blade_coords = section.coords
            else:
                blade_coords = np.concatenate(
                    (blade_coords, section.coords), axis=0)

        # plot 3d blade on plotView canvas
        # clear canvas
        self.plot_view_frame.destroy()
        self.plot_view_frame = ctk.CTkFrame(self.right_frame)
        self.plot_view_frame.pack(fill='both', expand=True, padx=10, pady=10)
        # plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(blade_coords[:, 0], blade_coords[:, 1], blade_coords[:, 2])
        # keep axes equal
        max_range = np.array([blade_coords[:, 0].max()-blade_coords[:, 0].min(), blade_coords[:, 1].max(
        )-blade_coords[:, 1].min(), blade_coords[:, 2].max()-blade_coords[:, 2].min()]).max() / 2.0
        mid_x = (blade_coords[:, 0].max()+blade_coords[:, 0].min()) * 0.5
        mid_y = (blade_coords[:, 1].max()+blade_coords[:, 1].min()) * 0.5
        mid_z = (blade_coords[:, 2].max()+blade_coords[:, 2].min()) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        # plot on canvas
        canvas = FigureCanvasTkAgg(fig, master=self.plot_view_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.plot_view_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
