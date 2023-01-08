import tkinter
from tkinter import filedialog
from matplotlib.figure import Figure
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from datfuncs2 import OpenTextFile, AddOnes, chordMult, prepend_line
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        # Configuration settings
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.GEOMETRY = f"{345}x{400}"
        self.TITLE = ".dat Converter 2 (Updated v6)"
        

        # Set up the main window
        self.geometry(self.GEOMETRY)
        self.resizable(0, 0)
        self.title(self.TITLE)
        self.view1()

    def view1(self):
        # Set up the file frame
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(padx=10, pady=10)

        # Set up the file location label and entry
        file_loc_label = ctk.CTkLabel(file_frame, text='File Location')
        file_loc_label.pack(anchor="w")
        file_loc_entry = ctk.CTkEntry(file_frame, placeholder_text='D:\\..', width=300)
        file_loc_entry.pack(fill="x", padx=2, pady=2)

        # Set up the file location open button
        self.FOLDER_ICON = ctk.CTkImage(light_image=Image.open("Assets/Folder.png"),
                                  dark_image=Image.open("Assets/Folder.png"))
        file_loc_open = ctk.CTkButton(file_frame, text='', width=20, image=self.FOLDER_ICON, command=self.open_file)
        file_loc_open.pack(padx=2, pady=2)

        # Set up the chord length label and entry
        chord_label = ctk.CTkLabel(file_frame, text='Chord Length')
        chord_label.pack(anchor="w")
        chord_entry = ctk.CTkEntry(file_frame, placeholder_text='160..')
        chord_entry.pack(fill="x", padx=2, pady=2)

        # Set up the load and plot buttons
        load_button = ctk.CTkButton(file_frame, text='Load', width=50, command=self.load_data)
        load_button.pack(padx=2, pady=2)
        plot_button = ctk.CTkButton(file_frame, text='Plot', width=50, command=self.plot_data)
        plot_button.pack(padx=2, pady=2)

        # Set up the save frame
        save_frame = ctk.CTkFrame(self)
        save_frame.pack(padx=10, pady=10)

        # Set up the save location label and entry
        save_loc_label = ctk.CTkLabel(save_frame, text='Save Location')
        save_loc_label.pack(anchor="w")
        save_loc_entry = ctk.CTkEntry(save_frame, placeholder_text='D:\\..', width=300)
        save_loc_entry.pack(fill="x", padx=2, pady=2)

        # Set up the save location open button
        save_loc_open = ctk.CTkButton(save_frame, text='', width=20, image=self.FOLDER_ICON, command=self.open_save_location)
        save_loc_open.pack(padx=2, pady=2)

        # Set up the save and convert buttons
        save_button = ctk.CTkButton(save_frame, text='Save', width=50, command=self.save_data)
        save_button.pack(padx=2, pady=2)
        convert_button = ctk.CTkButton(save_frame, text='Convert', width=50, command=self.convert_data)
        convert_button.pack(padx=2, pady=2)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        self.file_loc_entry.insert(0, file_path)

    def open_save_location(self):
        save_path = filedialog.askdirectory()
        self.save_loc_entry.insert(0, save_path)

    def load_data(self):
        file_path = self.file_loc_entry.get()
        chord_length = self.chord_entry.get()
        data = OpenTextFile(file_path, chord_length)
        self.raw_data = data
        self.x_values, self.y_values = AddOnes(data)

    def plot_data(self):
        x = self.x_values
        y = self.y_values
        fig = Figure(figsize=(5, 4), dpi=100)
        a = fig.add_subplot(111)
        a.plot(x, y)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

    def save_data(self):
        save_path = self.save_loc_entry.get()
        data = self.raw_data
        np.savetxt(save_path + '\converted.txt', data, delimiter=',')

    def convert_data(self):
        save_path = self.save_loc_entry.get()
        data = self.raw_data
        chord_length = self.chord_entry.get()
        converted_data = chordMult(data, chord_length)
        np.savetxt(save_path + '\converted.txt', converted_data, delimiter=',')
        prepend_line(save_path + '\converted.txt', 'Converted Data')

if __name__ == "__main__":
  app = App()
  app.mainloop()