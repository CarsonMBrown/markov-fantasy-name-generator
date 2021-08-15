from utils import menu, load_file, read_file, get_file_location


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
    file_location = get_file_location()
    lines = read_file(file_location)
    lines = "\n".join([lines[x].strip() for x in range(0, len(lines)) if x % m == r])
    f = load_file(file_location, "w")
    f.write(lines)


def clean_file(action):
    file_location = get_file_location()
    lines = "\n".join(map(action, read_file(file_location)))
    f = load_file(file_location, "w")
    f.write(lines)


if __name__ == "__main__":
    main()
