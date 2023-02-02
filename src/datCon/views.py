import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from config import *
from import_export import *
from graph import *
from txt_logic import *


def main_view(App):
    titles_font = ctk.CTkFont(family="Arciform", size=20)
    text_font = ctk.CTkFont(family="Arciform", size=12)
    # =====================FRAMING==================================================
    App.master_frame = ctk.CTkFrame(App)
    App.master_frame.pack(pady=5, padx=5, fill='both', expand=True)

    App.right_frame = ctk.CTkFrame(App.master_frame)
    App.right_frame.pack(side='right', fill='both',
                         expand=True, padx=5, pady=5)
    # ===============================================================================

    # =====================leftFrame==================================================
    App.tab_view = ctk.CTkTabview(App.master_frame)
    App.tab_view.pack(fill='both', expand=True,
                      padx=5, pady=5, side='left')
    App.config_tab = App.tab_view.add("Config")
    App.import_tab = App.tab_view.add("Import/Export")

    # =====================Config==================================================
    App.config_frame = ctk.CTkFrame(App.config_tab)
    App.config_frame.pack(fill='both', expand=True, padx=5, pady=5)

    # Config Widgets
    App.profile_frame = ctk.CTkFrame(App.config_frame)
    App.profile_frame.pack(fill='x', expand=True,
                           padx=5, pady=5, anchor='n')

    # section quantity
    App.num_of_profiles_INT = 1
    App.section_quantity_label = ctk.CTkLabel(
        App.profile_frame, text="Number of sections: ", font=text_font)
    App.section_quantity_label.pack(side='left', padx=5, pady=5)
    App.section_quantity_entry = ctk.CTkEntry(
        App.profile_frame, font=text_font, width=55)
    App.section_quantity_entry.pack(side='left', padx=5, pady=5)
    App.section_quantity_entry.insert(0, "1")

    # profile displacement
    App.profile_disp_label = ctk.CTkLabel(
        App.profile_frame, text="Displacement", font=text_font)
    App.profile_disp_label.pack(side='left', padx=5, pady=5)
    App.profile_disp_entry = ctk.CTkEntry(
        App.profile_frame, font=text_font, width=55)
    App.profile_disp_entry.pack(side='left', padx=5, pady=5)
    App.profile_disp_entry.insert(0, "0")

    # set button
    App.set_button = ctk.CTkButton(
        App.profile_frame, text="Set", font=text_font, command=lambda: change_number_of_profile_event(App.section_quantity_entry, App.section_select_option))
    App.set_button.pack(side='right', padx=5, pady=5)

    # profile config frame
    App.profile_config_frame = ctk.CTkFrame(App.config_frame)
    App.profile_config_frame.pack(
        fill='x', expand=True, padx=5, pady=5, anchor='n')

    # section select
    App.section_select_label = ctk.CTkLabel(
        App.profile_config_frame, text="Section: ", font=text_font)
    App.section_select_label.pack(side='left', padx=5, pady=5)
    App.section_select_option = ctk.CTkOptionMenu(App.profile_config_frame, values=[
        "1"], font=text_font, width=55)
    App.section_select_option.pack(side='left', padx=5, pady=5)
    App.section_select_option.set(1)

    # profile Twist
    App.section_twist_label = ctk.CTkLabel(
        App.profile_config_frame, text="Twist: ", font=text_font)
    App.section_twist_label.pack(side='left', padx=5, pady=5)
    App.section_twist_entry = ctk.CTkEntry(
        App.profile_config_frame, font=text_font, width=55)
    App.section_twist_entry.pack(side='left', padx=5, pady=5)
    App.section_twist_entry.insert(0, "0")

    # profile Chord
    App.section_chord_label = ctk.CTkLabel(
        App.profile_config_frame, text="Chord: ", font=text_font)
    App.section_chord_label.pack(side='left', padx=5, pady=5)
    App.section_chord_entry = ctk.CTkEntry(
        App.profile_config_frame, font=text_font, width=55)
    App.section_chord_entry.pack(side='left', padx=5, pady=5)
    App.section_chord_entry.insert(0, "1")

    # profile select
    App.profile_select_label = ctk.CTkLabel(
        App.profile_config_frame, text="Profile: ", font=text_font)
    App.profile_select_label.pack(side='left', padx=5, pady=5)

    # list of profile txt files in the profile folder
    App.profile_list = []
    App.profile_list = list_profiles(App.profile_list)

    App.profile_select_option = ctk.CTkOptionMenu(
        App.profile_config_frame, values=App.profile_list, font=text_font, width=55)
    App.profile_select_option.pack(side='left', padx=5, pady=5)
    App.profile_select_option.set("")

    # profile save button
    App.profile_save_button = ctk.CTkButton(
        App.profile_config_frame, text="Save", font=text_font, command=lambda: save_section_config_event(App.current_blade, App.section_select_option, App.profile_disp_entry, App.section_twist_entry, App.section_chord_entry, App.profile_select_option))
    App.profile_save_button.pack(side='right', padx=5, pady=5)

    # save Blade Frame
    App.save_blade_frame = ctk.CTkFrame(App.config_frame)
    App.save_blade_frame.pack(
        fill='x', expand=True, padx=5, pady=5, anchor='n')

    # save Blade Button
    App.save_blade_button = ctk.CTkButton(
        App.save_blade_frame, text="Save Blade", font=text_font, command=lambda: save_blade_event(App.save_blade_name_entry, App.current_blade))
    App.save_blade_button.pack(side='right', padx=5, pady=5)

    # save Blade Name Entry
    App.save_blade_name_entry = ctk.CTkEntry(
        App.save_blade_frame, font=text_font, width=100)
    App.save_blade_name_entry.pack(side='right', padx=5, pady=5)
    App.save_blade_name_entry.insert(0, "Blade Name")

    # plot Blade Frame
    App.plot_blade_frame = ctk.CTkFrame(App.config_frame)
    App.plot_blade_frame.pack(
        fill='x', expand=True, padx=5, pady=5, anchor='n')
    # plot Blade Button
    App.plot_blade_button = ctk.CTkButton(
        App.plot_blade_frame, text="Plot Blade", font=text_font, command=lambda: plot_blade_event(App.current_blade, App.right_frame))
    App.plot_blade_button.pack(side='right', padx=5, pady=5)

    # load Blade Frame
    App.load_blade_frame = ctk.CTkFrame(App.config_frame)
    App.load_blade_frame.pack(
        fill='x', expand=True, padx=5, pady=5, anchor='n')
    # load Blade Button
    App.load_blade_button = ctk.CTkButton(
        App.load_blade_frame, text="Load Blade", font=text_font, command=lambda: load_blade_event(App))
    App.load_blade_button.pack(side='right', padx=5, pady=5)

    # print blade button
    App.print_blade_button = ctk.CTkButton(
        App.load_blade_frame, text="Print Blade", font=text_font, command=lambda: print_blade_event(App.current_blade))
    App.print_blade_button.pack(side='right', padx=5, pady=5)

    # =====================Save/Load==================================================
    App.save_load_frame = ctk.CTkFrame(App.import_tab)
    App.save_load_frame.pack(fill='both', expand=True, padx=5, pady=5)

    # Save/Load Widgets
    App.nested_save_frame = ctk.CTkFrame(App.save_load_frame)
    App.nested_save_frame.pack(fill='both', expand=True, padx=5, pady=5)

    App.folder_icon = ctk.CTkImage(
        light_image=Image.open("Assets/Folder.png"))
    App.file_loc_label = ctk.CTkLabel(
        App.nested_save_frame, text='Import .dat File Location:')
    App.file_loc_label.grid(
        row=0, column=0, columnspan=3, sticky='nsew', pady=2)

    App.file_loc_entry = ctk.CTkEntry(
        App.nested_save_frame, placeholder_text='C:\\..', width=300)
    App.file_loc_entry.grid(
        row=1, column=0, sticky='nsew', pady=2, columnspan=2)

    App.file_loc_open = ctk.CTkButton(
        App.nested_save_frame, text='', width=20, image=App.folder_icon, command=lambda: open_file_location_event(App.file_loc_entry))
    App.file_loc_open.grid(row=1, column=2, sticky='nsew', pady=2)

    App.file_name_label = ctk.CTkLabel(
        App.nested_save_frame, text='File Name')
    App.file_name_label.grid(row=2, column=0, sticky='nsew', pady=2)

    App.import_name_entry = ctk.CTkEntry(
        App.nested_save_frame, placeholder_text='NACAXXXX..')
    App.import_name_entry.grid(row=3, column=0, sticky='nsew', pady=2)

    App.import_save = ctk.CTkButton(
        App.nested_save_frame, text='Save', width=50, command=lambda: save_profile_event(App.import_name_entry, App.file_loc_entry))
    App.import_save.grid(row=3, column=1, columnspan=3, sticky='nsew')

    App.save_loc_label = ctk.CTkLabel(
        App.nested_save_frame, text='Export SC compatible Save Location:')
    App.save_loc_label.grid(
        row=4, column=0, columnspan=3, sticky='nsew', pady=2)

    App.save_loc_entry = ctk.CTkEntry(
        App.nested_save_frame, placeholder_text='D:\\..', width=300)
    App.save_loc_entry.grid(
        row=5, column=0, sticky='nsew', pady=2, columnspan=2)

    App.save_loc_open = ctk.CTkButton(
        App.nested_save_frame, text='', width=20, image=App.folder_icon, command=lambda: open_save_location_event(App.save_loc_entry))
    App.save_loc_open.grid(row=5, column=2, sticky='nsew', pady=2)

    App.file_name_label = ctk.CTkLabel(
        App.nested_save_frame, text='File Name')
    App.file_name_label.grid(row=6, column=0, sticky='nsew', pady=2)

    App.export_name_entry = ctk.CTkEntry(
        App.nested_save_frame, placeholder_text='NACAXXXX..')
    App.export_name_entry.grid(row=7, column=0, sticky='nsew', pady=2)

    App.file_save = ctk.CTkButton(
        App.nested_save_frame, text='Save', width=50, command=lambda: export_curves_event(App.current_blade, App.save_loc_entry, App.export_name_entry))
    App.file_save.grid(row=7, column=1, columnspan=3, sticky='nsew')

    # =====================rightFrame==================================================
