import os
import codecs

def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def get_file_location(file_type="txt"):
    return f"../input/{input(f'Enter File Name: ')}"


def load_file(file_location="", access_type="r", file_type="txt"):
    if not file_location:
        file_location = get_file_location(file_type)
    open(f"{file_location}.{file_type}")
    return codecs.open(f"{file_location}.{file_type}", encoding='utf-8', mode=access_type)


def read_file(file_location="", access_type="r", file_type="txt"):
    return load_file(file_location, access_type, file_type).readlines()


def menu(title, options, actions, arg=None):
    clear_console()
    should_exit = False
    should_print_options = True
    num_options = len(options)
    while not should_exit:
        if should_print_options:
            print(title)
            for i in range(num_options):
                print(f"  {str(i + 1)}. {options[i]}")
            should_print_options = False
        choice = input("Choice: ").strip()
        action_preformed = False
        for i in range(num_options):
            if choice == str(i + 1):
                action_preformed = True
                if len(actions) > i:
                    if arg is None:
                        actions[i]()
                    else:
                        actions[i](arg)
                else:
                    should_exit = True
                should_print_options = True
        if not action_preformed:
            print("Please Choose A Valid ", end='')