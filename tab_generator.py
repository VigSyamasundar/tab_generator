from project import generate_new_project

#-----------------------------------------
# Global variables
#-----------------------------------------
num_strings = 0
low_high_tuning = ""
tab = []
max_tab_entry_size = []
tab_intro_separator = " |"
tab_intro_offset = len(tab_intro_separator)
tab_entry_separator = " -- "
serial_intro_separator = "# |"
tab_len = 0
tab_len_incl_sep = 0
serial = ""


VERSION = 0.1


def log_error(error_message, level):
    if (level == "low"):
        print("Warning:", error_message)
    elif (level == "fatal"):
        print("Fatal:", error_message)
        exit()
    else:
        print("Unknown error: ", error_message)
        exit()

# gets tab tuning and errors if more than num_strings notes are specified
def retrieve_and_parse_tuning():
    global num_strings
    global low_high_tuning

    num_strings = input("Enter number of strings (example '6'): ")
    if (num_strings == ""):
        # Use default as 6 for guitar
        num_strings = 6
    print("")
    try: 
        num_strings = int(num_strings)
        if (num_strings < 1):
            log_error("Number of strings must be at least 1", "fatal")
    except:
        log_error("Number of strings specified is not a number", "fatal")

    low_high_tuning = input("Enter tuning from low to high seperated by a space (example 'E A D G B e'): ")
    if (low_high_tuning == ""):
        # Use standard tuning as default
        low_high_tuning = "E A D G B e"
    print("")
    low_high_tuning = low_high_tuning.split()
    if (len(low_high_tuning) != num_strings):
        log_error("Notes specified in the tuning does not match number of strings", "fatal")


def create_tab():
    for string_num in range(num_strings):
        tab.append([low_high_tuning[string_num]])


def record_frame(edit,frame_num):
    frame = []

    print("Recording new frame, enter fret for each string (low to high).")
    print("")
    for note in low_high_tuning:
        temp_fret = input(note + ": ")
        # if empty fret specified, change to '-'
        if (temp_fret == ""):
            temp_fret = "-"
        frame.append(temp_fret)

    if (edit):
        for string_num in range(num_strings):
            tab[string_num][frame_num] = frame[string_num] 
    else:
        for string_num in range(num_strings):
            tab[string_num].append(frame[string_num]) 
    print("")


def display_current_tab(disp_not_export):
    global tab_len
    global tab_len_incl_sep
    global serial
    global max_tab_entry_size

    for string_num in range(num_strings-1, -1, -1):
        for entry_idx in range(len(tab[string_num])):
            # create base entry tab max size
            if (entry_idx > 0):
                tab[string_num][entry_idx].replace(" ", "")


    for string_num in range(num_strings-1, -1, -1):
        temp_tab_entry_size = 0
        for entry_idx in range(len(tab[string_num])):
            # create base entry tab max size
            if (string_num == num_strings-1):
                max_tab_entry_size.append(len(tab[string_num][entry_idx]))

            # update tab_entry_size comparing with ever new entry
            if (len(tab[string_num][entry_idx]) > max_tab_entry_size[entry_idx]):
                max_tab_entry_size[entry_idx] = len(tab[string_num][entry_idx])
            
            # update tab_entry_size comparing with ever new entry
            if (len(str(entry_idx)) > max_tab_entry_size[entry_idx]):
                max_tab_entry_size[entry_idx] = int(len(str(entry_idx)))

        
    for string_num in range(num_strings-1, -1, -1):
        # temporary list and string for each strings tab
        temp_string_tab = []
        temp_string_tab_s = ""

        for entry_idx in range(len(tab[string_num])):
            entry_size_diff = 0

            if (entry_idx > 1):
                if (len(tab[string_num][entry_idx]) < max_tab_entry_size[entry_idx]):
                    entry_size_diff = max_tab_entry_size[entry_idx] - len(tab[string_num][entry_idx])
            
            if (entry_idx == 0):
                temp_string_tab.append(tab[string_num][entry_idx])
                temp_string_tab.append(tab_intro_separator)
                temp_string_tab.append(tab_entry_separator)
            else:
                temp_string_tab.append(" "*entry_size_diff)
                temp_string_tab.append(tab[string_num][entry_idx])
                temp_string_tab.append(tab_entry_separator)

        temp_string_tab_s = "".join(temp_string_tab)
        # capture max tab length
        if (len(temp_string_tab_s) > tab_len_incl_sep):
            tab_len_incl_sep = len(temp_string_tab_s)
        
        if (disp_not_export):
            print(temp_string_tab_s)
    
        if (len(tab[string_num]) > tab_len):
            tab_len = len(tab[string_num])

    # series of '-' to seperate tab and serial count
    if (disp_not_export):
        print("-"*tab_len_incl_sep)

    serial_tab = serial_intro_separator + tab_entry_separator

    for num in range(1,tab_len):
        serial_entry_size_diff = max_tab_entry_size[num] - len(str(num))
        serial_entry_size_diff_char = " "*serial_entry_size_diff
        serial_tab = serial_tab + serial_entry_size_diff_char + str(num) + tab_entry_separator
    if (disp_not_export):
        print(serial_tab)
    print("")


def edit_frame():
    frame_num = input("Enter frame to edit: ")
    try:
        frame_num = int(frame_num)
    except:
        log_error("Frame selection for edit must be a number", "low")
        return
    record_frame(1,frame_num)


def main():
    display_welcome_prompt()
    tab_project = get_new_or_existing_project()
    retrieve_and_parse_tuning()
    create_tab()
    while command != "save":
        command = input("1. new (enter a new tab frame) \n2. view (view entire recorded tab) \n3. edit (edit a frame) \n4. save (export tab as a txt file) \nEnter command: ")
        command = command.lower()
        print("")
        if (command == "new" or command == "n"):
            record_frame(0,0)
        elif (command == "edit" or command == "e"):
            edit_frame()
        elif (command == "view" or command == "v"):
            display_current_tab(1)
        elif (command == "save" or command == "s"):
            exit()


def display_welcome_prompt():
    print(f"Welcome to Easy Tabs v{VERSION}!")


def get_new_or_existing_project():
    print("""
        Please select from the following options:
        1 - Create a new project
        2 - Open an existing project
    """)
    selection = get_valid_selection()
    if selection == "1":
        return create_new_project()
    return get_existing_project()


def get_valid_selection():
    selection = input("---> ")

    def selection_is_not_valid(s):
        return s != "1" or s != "2"

    while selection_is_not_valid(selection):
        print("Please enter a valid selection. Please.")
        selection = input("---> ")
    return selection


def create_new_project():
    print("""
        Please name new project:
    """)
    project_name = input("---> ")
    return generate_new_project(project_name)


# main function
if __name__ == '__main__':
    main()
