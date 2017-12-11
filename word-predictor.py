from collections import defaultdict
import nltk
import pdb
import argparse
import codecs

def build_conditional_probabilities(corpus):
    """
    The function takes as its input a corpus string (words separated by 
    spaces) and returns a 2D dictionary of probabilities P(next|current) of
    seeing a word "next" conditionnaly to seeing a word "current". 
    """

    # First we parse the string to build a double dimension dictionary that
    # returns the conditional probabilities.

    # We parse the string to build a first dictionary indicating for each
    # word, what are the words that follow it in the string. Repeated next
    # words are kept so we use a list and not a set. 

    tokenized_string = corpus.split()
    previous_word = ""
    dictionary = defaultdict(list)

    for current_word in tokenized_string:
        if previous_word != "":
            dictionary[previous_word].append(current_word)
        previous_word = current_word
        
    # We know parse dictionary to compute the probability each observed
    # next word for each word in the dictionary. 

    for key in dictionary.keys():
        next_words = dictionary[key]
        unique_words = set(next_words) # removes duplicated
        nb_words = len(next_words)
        probabilities_given_key = {}
        for unique_word in unique_words:
            probabilities_given_key[unique_word] = \
                float(next_words.count(unique_word)) / nb_words
        dictionary[key] = probabilities_given_key

    return dictionary


def bigram_next_word_predictor(conditional_probabilities, current, next_candidate):
    """
    The function takes as its input a 2D dictionary of probabilities 
    P(next|current) of seeing a word "next" conditionnaly to seeing a word 
    "current", the current word being read, and a next candidate word, and
    returns P(next_candidate|current).
    """

    # We look for the probability corresponding to the 
    # current -> next_candidate pair

    if conditional_probabilities.has_key(current):
        if conditional_probabilities[current].has_key(next_candidate):
            return conditional_probabilities[current][next_candidate]

    # If current -> next_candidate pair has not been observed in the corpus,
    # the corresponding dictionary keys will not be defined. We return 
    # a probability 0.0

    return 0.0

def process_test_file(test_filename):
    """
    <p>Reads and processes the test file one word at a time. </p>

    :param test_filename: The name of the test corpus file.
    :return: <code>true</code> if the entire file could be processed, false otherwise.
    """
    try:
        with codecs.open(test_filename, 'r', 'utf-8') as f:
            tokens = nltk.word_tokenize(f.read().lower()) # Important that it is named tokens for the --check flag to work
            # for token in tokens:
                # compute_entropy_cumulatively(token)

            # take average using N (number of tokens in test corpus)
            # logProb = -logProb/test_words_processed
            # print(test_words_processed)
        return tokens
    except IOError:
        print('Error reading testfile')
        return False

def main():
    # An example corpus to try out the function

    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--corpus', '-t', type=str, required=True, help='test corpus')
    parser.add_argument('--check', action='store_true', help='check if your alignment is correct')

    arguments = parser.parse_args()
    # pdb.set_trace()
    corpus = process_test_file(arguments.corpus)
    # corpus = "the cat is red the cat is green the cat is blue the dog is brown"
    
    bigrams = nltk.ngrams(corpus, 2)

    pdb.set_trace() 

    # We call the conditional probability dictionary builder function
    conditional_probabilities = build_conditional_probabilities(corpus)
    
    print(conditional_probabilities)
    # Some sample queries to the bigram predictor
    assert bigram_next_word_predictor(conditional_probabilities, "the", "cat") == 0.75
    assert bigram_next_word_predictor(conditional_probabilities, "is", "red") == 0.25
    assert bigram_next_word_predictor(conditional_probabilities, "", "red") == 0.0

if __name__ == "__main__":
    main()