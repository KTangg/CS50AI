import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S NP | S Conj S | S PP S | S PP NP | NP PP NP
AP -> Adj | Adj AP
NP -> N | AP NP | Det N | NP PP | Det AP NP
PP -> P | P NP 
VP -> V | Adv VP | VP Adv | VP PP | VP PP NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize(parsing word)
    tmp = nltk.word_tokenize(sentence)
    words = []
    print(f"Token: {tmp}")

    # Preprocess
    for word in tmp:
        cnt = 0

        # Check if all letter is non alpha
        for letter in word:
            if not letter.isalpha():
                cnt += 1
        if cnt == len(word):
            continue
        
        # Lowercase and Add
        word = word.lower()
        words.append(word)

    print(f"Preprocessed: {words}")
    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks_list = []
    # Listing all NP in sentence with only one noun
    for np in tree.subtrees(lambda t: t.label() == "NP"):
        dup = False
        cnt = 0
        # Only one Noun in Noun Phase
        for n in np.subtrees(lambda t: t.label() == "N"):
            cnt += 1
        if cnt == 1:
            # Check for duplicate
            for chunk in chunks_list:
                for np_tree in chunk.subtrees(lambda t: t.label() == "NP"):
                    if np == np_tree:
                        dup = True
            if not dup:
                chunks_list.append(np)
    #print(f"Chunks After NP: {chunks_list}")
    # Check for left over stand alone noun
    for n in tree.subtrees(lambda t: t.label() == "N"):
        dup = False
        for chunk in chunks_list:
            #print(f"Chunk: {chunk}")
            # Check for duplicate
            for n_tree in chunk.subtrees(lambda t: t.label() == "N"):
                #print(f"Checking: {n} with {n_tree}")
                if n == n_tree:
                    #print(f"Equal: {n} with {n_tree}")
                    dup = True
                    break
        if not dup:
            chunks_list.append(n)

    return chunks_list

if __name__ == "__main__":
    main()
