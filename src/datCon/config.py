import array_logic
import classes


def change_number_of_profile_event(section_quantity_entry, section_select_option) -> None:
    """Updates the options in the profile select option menu based on the value of profile quantity entry."""
    num_of_profiles = int(section_quantity_entry.get())
    options = [str(i) for i in range(1, num_of_profiles + 1)]
    section_select_option.configure(values=options)


def save_section_config_event(current_blade, section_select_option, profile_disp_entry, section_twist_entry, section_chord_entry, profile_select_option) -> None:
    """Saves the configuration of a section to the current blade object."""
    section_index = int(section_select_option.get())
    section_displacement = float(profile_disp_entry.get())
    section_twist = float(section_twist_entry.get())
    section_chord = float(section_chord_entry.get())

    profile_name = profile_select_option.get()
    with open("Profiles/" + profile_name + ".txt") as f:
        section_profile = array_logic.strip_profile_to_array(f)

    section_coords = array_logic.calculate_section_coords(
        section_profile, section_chord, section_twist, section_displacement, section_index
    )

    temp_section = classes.Section(
        section_index, section_displacement, section_twist, section_chord, section_profile, section_coords
    )
    current_blade.add_section(temp_section)
