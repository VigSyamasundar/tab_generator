from tab_utils import Tab


def generate_new_project(project_name):
    tuning, string_count = get_tuning_and_string_count_params()
    tab = Tab(project_name, string_count, tuning, frames=[])
    create_new_tab_file(project_name)
    return tab


def create_new_tab_file(project_name):
    open(f"{project_name}.json", "a").close()


def get_tuning_and_string_count_params():
    string_count = input("Enter number of strings: (default 6)")
    if not string_count:
        string_count = 6
    else:
        string_count = int(string_count)

    tuning = input("Enter tuning from low to high separated by space: (default 'E A D G B e') ")
    if not tuning:
        tuning = ["E", "A", "D", "G", "B", "e"]
    else:
        tuning = tuning.split()
    return tuning, string_count
