from markov_chain import MarkovChain


def menu(options, actions, arg=None):
    should_exit = False
    should_print_options = True
    num_options = len(options)
    while not should_exit:
        if should_print_options:
            for i in range(num_options):
                print(f"  {str(i + 1)}. {options[i]}")
            should_print_options = False
        choice = input("Choice: ").strip()
        for i in range(num_options):
            if choice == str(i + 1):
                if arg is None:
                    actions[i]()
                else:
                    actions[i](arg)
                should_print_options = True


def main_menu():
    print("Markov Chain Fantasy Name Generator")
    should_exit = False
    should_print_options = True
    while not should_exit:
        if should_print_options:
            print("  1. Create New Markov Chain")
            print("  2. Load Existing Markov Chain From File")
            print("  3. Quit")
            should_print_options = False
        choice = input("Choice: ")
        if choice.strip()[0:1] == "1":
            chain_menu(new_chain())
            should_print_options = True
        elif choice.strip()[0:1] == "2":
            chain_menu(load_chain())
            should_print_options = True
        elif choice.strip()[0:1] == "3":
            should_exit = True
        else:
            print("Please Choose A Valid ", end='')


def chain_menu(chain):
    print("Markov Chain Menu")
    should_exit = False
    should_print_options = True
    while not should_exit:
        if should_print_options:
            print("  1. Train")
            print("  2. Generate")
            print("  3. Back")
            should_print_options = False
        choice = input("Choice: ")
        if choice.strip()[0:1] == "1":
            train(chain)
            should_print_options = True
        elif choice.strip()[0:1] == "2":
            generate(chain)
            should_print_options = True
        elif choice.strip()[0:1] == "3":
            should_exit = True
        else:
            print("Please Choose A Valid ", end='')


def train(chain):
    print("Markov Chain Training Menu")


def generate(chain):
    print("Markov Chain Generation Menu")


def new_chain():
    print("Creating A New Markov Chain")
    n_gram_size = "Not A Number"
    while not n_gram_size.isnumeric():
        n_gram_size = input("N-Gram Size: ")
    n_gram_size = int(n_gram_size)
    chain = MarkovChain(n_gram_size)
    print(f"New Empty Markov Chain Using {n_gram_size}-Grams Created.")
    chain_menu(chain)


def load_chain():
    pass
