from utils import menu, load_file, read_file, get_file_location, INPUT_FOLDER, write_file


def main():
    main_menu()


def main_menu():
    menu("How Do You Want To Clean Files?",
         ["Keep First Words", "Keep Odd Lines", "Keep Even Lines"],
         [first_words, every_even_line, every_odd_line])


def first_words():
    clean_file(lambda x: x.split()[0:][0].strip())


def every_even_line():
    every_x_lines(2, 0)


def every_odd_line():
    every_x_lines(2, 1)


def every_x_lines(m, r):
    file_name = get_file_location()
    lines = read_file(file_name, INPUT_FOLDER)
    write_file(
        "\n".join([lines[x].strip() for x in range(0, len(lines)) if x % m == r]),
        file_name, INPUT_FOLDER
    )


def clean_file(action):
    file_name = get_file_location()
    write_file(
        "\n".join(map(action, read_file(file_name, INPUT_FOLDER))),
        file_name, INPUT_FOLDER
    )


if __name__ == "__main__":
    main()
