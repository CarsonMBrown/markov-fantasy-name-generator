import json

from markov_chain import MarkovChain
from data_cleaner import main as cleaner_menu
from utils import menu, read_file, print_line, TAB, INPUT_FOLDER, SAVE_FOLDER


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
         chain,
         True)


def train_chain_file(chain):
    for line in read_file(folder=INPUT_FOLDER):
        clean_line = line.strip()
        print(f"{TAB}{clean_line}: {chain.train(clean_line)}")
    print(f"{TAB}Training Finished")


def train_chain_console(chain):
    print("Enter Training Data:")
    while chain.train(input("  ")):
        continue
    print(f"{TAB}Training Finished")


def generate_chain(chain):
    print("Generating...")
    print_line()
    for i in range(10):
        print(chain.generate())
    print_line()


def inspect_chain(chain):
    print("Markov Chain Inspection Menu")
    print(", ".join([state.get_info() for state in
                     chain.get_state_chain(input(f"{TAB}State Chain To Inspect: "))[1:]]))


def print_chain(chain):
    print(chain)


def save_chain(chain):
    chain.save()


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
    load_json = json.loads("".join(read_file(folder=SAVE_FOLDER, file_type="json")))
    print(load_json)
    chain_menu(MarkovChain(load_json))
