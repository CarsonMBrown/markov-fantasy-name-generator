import nltk
from nltk.util import ngrams as create_ngrams

ALPHABET = [chr(letter) for letter in range(ord('a'), ord('z') + 1)]
ADDITIONAL_ALLOWED_CHARS = [
    " ", "\'", "_"
]
ALLOWED_CHARS = ALPHABET + ADDITIONAL_ALLOWED_CHARS


class MarkovChain:
    def __init__(self, n):
        self.n_gram_size = n
        self.matrix = MarkovState("ROOT")
        for character in ALLOWED_CHARS:
            self.matrix.add_child(character)
        for i in range(n-1):
            for leaf in self.matrix.get_leaves():
                for character in ALLOWED_CHARS:
                    leaf.add_child(character)

    def add_chance(self, state_identifier):
        for state in self.get_state_chain(state_identifier):
            state.add_occurrence()

    def add_chances(self, state_identifiers):
        for state_identifier in state_identifiers:
            self.add_chance(state_identifier)

    def get_state(self, state_identifier):
        print(self.get_state_chain(state_identifier)[-1])
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

    def train(self, data):
        data = f"__{data.lower()}_"
        for character in data:
            if character not in ALLOWED_CHARS:
                return False
        self.add_chances(["".join(ngram) for ngram in create_ngrams(data, self.n_gram_size)])

    def __str__(self):
        return "--------------------------------------------------------\n" \
               f"N-Gram Size: {self.n_gram_size}\n" \
               f"Total N-Grams Stored: {self.matrix.occurrences}\n" \
               "--------------------------------------------------------"

class MarkovState:
    def __init__(self, state_identifier, occurrences=0):
        self.state_identifier = state_identifier
        self.occurrences = occurrences
        self.children = []

    def add_child(self, child_state_identifier, child_probability=0):
        self.children.append(MarkovState(child_state_identifier, child_probability))

    def add_occurrence(self):
        self.occurrences += 1

    def get_leaves(self):
        leaves = []
        for child in self.children:
            if child.is_leaf():
                leaves.append(child)
            else:
                leaves += child.get_leaves()
        return leaves

    def is_leaf(self):
        return self.children == []

    def get_info(self):
        return f"({self.state_identifier}, {self.occurrences})"

    def get_state(self, state_identifier):
        for child in self.children:
            if child == state_identifier:
                return child
        return False

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