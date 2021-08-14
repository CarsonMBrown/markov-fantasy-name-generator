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


def main_menu():
    print("Markov Chain Fantasy Name Generator")
    menu(["Create New Markov Chain", "Load Existing Markov Chain From File", "Quit"],
         [new_chain, load_chain])


def chain_menu(chain):
    print("Markov Chain Menu")
    menu(["Train", "Generate", "Inspect", "Print", "Save", "Back"],
         [train_chain, generate_chain, inspect_chain, print_chain, save_chain],
         chain)


def train_chain(chain):
    print("Markov Chain Training Menu")
    print("Enter Training Data:")
    while chain.train(input()):
        continue
    print("Training Finished")


def generate_chain(chain):
    print("Markov Chain Generation Menu")


def inspect_chain(chain):
    print("Markov Chain Inspection Menu")
    print(", ".join([state.get_info() for state in chain.get_state_chain(input(" State Chain To Inspect: "))[1:]]))


def print_chain(chain):
    print(chain)


def save_chain(chain):
    pass


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
