import io
import os
import codecs

LINE_SEPARATOR = "-" * 16
TAB = "  "

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
SAVE_FOLDER = "markov_chains"


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def get_file_location():
    return input(f'Enter File Name: ')


def load_file(file_name="", folder="", access_type="r", file_type="txt"):
    if not file_name:
        file_name = get_file_location()
    return io.open(f"../{folder}/{file_name}.{file_type}", encoding='utf-8', mode=access_type)


def read_file(file_name="", folder="", file_type="txt"):
    f = load_file(file_name, folder, "r", file_type)
    file_content = f.readlines()
    f.close()
    return file_content


def write_file(output, file_name="", folder="", file_type="txt"):
    f = load_file(file_name, folder, "w", file_type)
    f.write(output)
    f.close()


def menu(title, options, actions, arg=None, is_single_choice_menu=False):
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
                    should_exit = is_single_choice_menu
                else:
                    should_exit = True
                should_print_options = True
        if not action_preformed:
            print("Please Choose A Valid ", end='')


def print_line():
    print(LINE_SEPARATOR)
