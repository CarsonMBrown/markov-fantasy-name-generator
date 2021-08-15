import json
import random

from nltk.util import ngrams as create_ngrams
from utils import LINE_SEPARATOR, TAB, write_file, SAVE_FOLDER

ALPHABET = [chr(letter) for letter in range(ord('a'), ord('z') + 1)]
ADDITIONAL_ALLOWED_CHARS = [
    " ", "\'", "_"
]
ALLOWED_CHARS = ALPHABET + ADDITIONAL_ALLOWED_CHARS


class MarkovState:
    def __init__(self, state_identifier, occurrences=0):
        self.state_identifier = state_identifier
        self.occurrences = occurrences
        self.children = []

    def add_child(self, child_state_identifier, child_probability=0):
        self.children.append(MarkovState(child_state_identifier, child_probability))

    def add_occurrence(self, num=1):
        self.occurrences += num

    def get_choices(self):
        return [child.state_identifier for child in self.children]

    def get_leaves(self):
        leaves = []
        for child in self.children:
            if child.is_leaf():
                leaves.append(child)
            else:
                leaves += child.get_leaves()
        return leaves

    def get_non_zero_leaves(self, previous_states=""):
        leaves = []
        for child in self.children:
            if child.is_leaf() and child.occurrences > 0:
                leaves.append((previous_states + child.state_identifier, child.occurrences))
            else:
                leaves += child.get_non_zero_leaves(previous_states + child.state_identifier)
        return leaves

    def get_non_zero_leaves_info(self):
        return [f"{leaf[0]}, {leaf[1]}" for leaf in self.get_non_zero_leaves()]

    def get_info(self):
        return f"({self.state_identifier}, {self.occurrences})"

    def get_state(self, state_identifier):
        for child in self.children:
            if child == state_identifier:
                return child
        return False

    def get_weights(self):
        return [child.occurrences for child in self.children]

    def is_leaf(self):
        return self.children == []

    def __eq__(self, other):
        if isinstance(other, str):
            return self.state_identifier == other
        return self == other

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        if self.children:
            return f"({self.state_identifier}, {self.occurrences}, [{', '.join(str(x) for x in self.children)}])"
        else:
            return f"({self.state_identifier}, {self.occurrences})"


class MarkovChain:
    N_GRAM_SIZE = "n-gram size"
    NON_TRIVIAL_N_GRAMS = "non-trivial-n-grams"
    prefix = ''
    suffix = '_'
    matrix = MarkovState("ROOT")

    def __init__(self, params):
        if isinstance(params, int):
            self.n_gram_size = params
        elif isinstance(params, dict):
            self.load(params)

    def add_chance(self, state_identifier, num=1):
        for state in self.get_state_chain(state_identifier):
            state.add_occurrence(num)

    def add_chances(self, state_identifiers):
        for state_identifier in state_identifiers:
            self.add_chance(state_identifier)

    def build_matrix(self):
        self.prefix = self.suffix * (self.n_gram_size - 1)
        for character in ALLOWED_CHARS:
            self.matrix.add_child(character)
        for i in range(self.n_gram_size - 1):
            for leaf in self.matrix.get_leaves():
                for character in ALLOWED_CHARS:
                    leaf.add_child(character)

    def clean_generated_text(self, text):
        text = text.replace(self.suffix, "")
        return text[0].capitalize() + text[1:]

    def load(self, load_json):
        self.n_gram_size = load_json[self.N_GRAM_SIZE]
        self.build_matrix()
        for n_gram in load_json[self.NON_TRIVIAL_N_GRAMS].keys():
            self.add_chance(n_gram, load_json[self.NON_TRIVIAL_N_GRAMS][n_gram])

    def generate(self, char_limit=20):
        generated_text = self.prefix
        while len(generated_text) - len(self.prefix) < char_limit:
            generated_text += self.get_next_char(generated_text[-self.n_gram_size + 1:])
            if generated_text.endswith(self.suffix):
                break
        return self.clean_generated_text(generated_text)

    def get_next_char(self, previous):
        state = self.get_state(previous)
        choice = random.choices(state.get_choices(), weights=state.get_weights())[0]
        return choice

    def get_state(self, state_identifier):
        return self.get_state_chain(state_identifier)[-1]

    def get_state_chain(self, state_identifier):
        states = [self.matrix]
        while state_identifier:
            next_state = states[-1].get_state(state_identifier[0:1])
            state_identifier = state_identifier[1:]
            if next_state:
                states.append(next_state)
            else:
                break
        return states

    def save(self):
        save_json = {self.N_GRAM_SIZE: self.n_gram_size, self.NON_TRIVIAL_N_GRAMS: {}}
        for leaf in self.matrix.get_non_zero_leaves():
            print(leaf)
            save_json[self.NON_TRIVIAL_N_GRAMS][leaf[0]] = leaf[1]
        write_file(json.dumps(save_json, indent=4), input("File Name:"), SAVE_FOLDER, "json")

    def train(self, data):
        if not data:
            return False
        data = f"{self.prefix}{data.lower()}{self.suffix}"
        for character in data:
            if character not in ALLOWED_CHARS:
                return False
        self.add_chances(["".join(ngram) for ngram in create_ngrams(data, self.n_gram_size)])
        return True

    def __str__(self):
        break_tab = f"\n{TAB}"
        return f"{LINE_SEPARATOR}\n" \
               f"N-Gram Size: {self.n_gram_size}\n" \
               f"Total N-Grams Stored: {self.matrix.occurrences}\n" \
               f"{TAB}{break_tab.join(self.matrix.get_non_zero_leaves_info())}\n" \
               f"{LINE_SEPARATOR}"
