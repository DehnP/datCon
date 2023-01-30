import array_logic
import classes


def change_number_of_profile_event(section_quantity_entry, section_select_option) -> None:
    print("change_number_of_profile_event")
    # get value from profile quantity entry
    num_of_profiles_INT = int(section_quantity_entry.get())
    options = [str(i) for i in range(1, num_of_profiles_INT+1)]
    # update the options in the profile select option menu
    section_select_option.configure(values=options)


def save_section_config_event(current_blade, section_select_option, profile_disp_entry, section_twist_entry, section_chord_entry, profile_select_option) -> None:
    # Save configuration of section
    print("save_profile_event")
    # get values from entry boxes
    section_index = int(section_select_option.get())
    section_displacement = float(profile_disp_entry.get())
    section_twist = float(section_twist_entry.get())
    section_chord = float(section_chord_entry.get())
    # strip the .txt from the profile name
    temp_profile_name = profile_select_option.get()
    section_profile = array_logic.strip_profile_to_array(
        "Profiles/" + temp_profile_name + ".txt")

    # generate coords for profile
    section_coords = array_logic.scale_profile(
        section_profile, section_chord)
    section_coords = array_logic.rotate_profile(
        section_coords, section_twist)
    section_coords = array_logic.add_displacement_column(
        section_coords, section_index, section_displacement)

    # save to class 'section' object
    temp_section = classes.Section(section_index, section_displacement,
                                   section_twist, section_chord, section_profile, section_coords)

    # save to class 'blade' object
    current_blade.add_section(temp_section)

    print(temp_section)
    print(current_blade.sections)
