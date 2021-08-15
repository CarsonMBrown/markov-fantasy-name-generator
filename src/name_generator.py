from markov_chain import MarkovChain
from data_cleaner import main as cleaner_menu
from utils import menu, read_file, load_file


def main_menu():
    menu("Markov Chain Fantasy Name Generator",
         ["Create New Markov Chain", "Load Existing Markov Chain From File", "Clean File", "Quit"],
         [new_chain, load_chain, cleaner_menu])


def chain_menu(chain):
    menu("What Do You Want To Do With The Markov Chain?",
         ["Train", "Test Generate", "Inspect", "Print", "Save", "Back"],
         [train_chain, generate_chain, inspect_chain, print_chain, save_chain],
         chain)


def train_chain(chain):
    menu("How Do You Want To Train The Markov Chain?",
         ["File", "Console", "Back"],
         [train_chain_file, train_chain_console],
         chain)


def train_chain_file(chain):
    for line in read_file():
        clean_line = line.strip()
        print(f"  {clean_line}: {chain.train(clean_line)}")
    print("  Training Finished")


def train_chain_console(chain):
    print("Enter Training Data:")
    while chain.train(input("  ")):
        continue
    print("  Training Finished")


def generate_chain(chain):
    print("Generating...")
    print("--------------------------------------------------------")
    for i in range(10):
        print(chain.generate())
    print("--------------------------------------------------------")


# def generate_dump_chain(chain):
#     f = load_file()
#     print("Generating...")
#     for i in range(100):
#         f.write(chain.generate() + "\n")


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
