from os import remove, rename, listdir


def add_blank_line(file_path) -> None:
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        line_count = 1
        for line in lines:
            file.write(line)
            if line_count % 35 == 0:
                file.write("\n")
            line_count += 1


def prepend_line_to_file(file_path, line) -> None:
    dummy_file = file_path + '.bak'
    with open(file_path, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        write_obj.write(line + '\n')
        for line in read_obj:
            write_obj.write(line)
    remove(file_path)
    rename(dummy_file, file_path)


def list_profiles(profile_list) -> list:
    # list all profiles in the profile folder
    profile_list = []
    for file in listdir("Profiles"):
        if file.endswith(".txt"):
            profile_list.append(file.replace(".txt", ""))
    return profile_list
