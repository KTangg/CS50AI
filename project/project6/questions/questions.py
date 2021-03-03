import math
import nltk
import string
import sys
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens
    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    # Open Directory
    with os.scandir(directory) as corpus_dir:
        # Open Each file
        for corpus in corpus_dir:
            # Add {filename: content}
            with open(os.path.join(directory, corpus.name), encoding="utf8") as f:
                print(f"Open: {os.path.join(directory, corpus.name)}")
                content = f.read()
            files[corpus.name] = content

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # token the document
    tmp = nltk.word_tokenize(document)
    # Declare stopwords and punctuation to remove
    punctuation = [x for x in string.punctuation]
    stopword = nltk.corpus.stopwords.words("english")

    words = list()
    # Check everyword
    for word in tmp:
        word = word.lower()
        # Check stopwords and punctuation
        if (word not in punctuation) and (word not in stopword):
            words.append(word)
    
    # Order the list
    words.sort()
    
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_idf = dict()
    # Total documents
    total_doc = len(documents)
    # Check each document
    for document in documents:
        words = documents[document]
        # Check each word
        for word in words:
            # Not compute word that already computed
            if word not in words_idf:
                # Compute document that word appear
                appear_doc = 0
                for check_doc in documents:
                    if word in documents[check_doc]:
                        appear_doc += 1
                # Compute IDF and add to IDF dict
                idf = math.log(total_doc / appear_doc)
                words_idf[word] = idf

    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Declare TF-IDF list value
    tf_idfs = list()
    # Check every document
    for document in files:
        # Count for word frequent
        word_cnt = {word:files[document].count(word) for word in files[document]}
        # Check for each word in query
        total_tf_idf = 0
        for word in query:
            if word in word_cnt:
                tf = word_cnt[word]
                # Compute tf-idf
                word_tf_idf = tf * (idfs[word])
                total_tf_idf += word_tf_idf
        tf_idfs.append((document, total_tf_idf))
    # Sort TF-IDFS base on value
    tf_idfs.sort(key = lambda x: x[1], reverse = True)
    # List top n-document
    result = [tf_idf[0] for tf_idf in tf_idfs[:n]]

    return result
    
    
def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Declare IDF list value
    #print(idfs)
    total_idfs = list()
    # Check every sentences
    for sentence in sentences:
        # Check for each word in query
        word_in_sent = 0
        total_idf = 0
        #print(f"Check {query} In {sentence}")
        for word in query.copy():
            sentence_words = tokenize(sentence)
            if word in sentence_words:
                #print(f"{word} is in {sentence}")
                # Add word in sentence
                word_in_sent += 1
                # Compute idf
                total_idf += idfs[word]
        word_dense = word_in_sent / len(sentence_words)
        total_idfs.append((sentence, total_idf, word_dense, word_in_sent))
    # Sort IDFS base on value
    total_idfs.sort(key = lambda x: (x[1], x[2]), reverse = True)
    #print(f"Sentence IDF: {total_idfs}")
    # List top n-sentence
    result = [idf[0] for idf in total_idfs[:n]]
    return result


if __name__ == "__main__":
    main()
